"""
Legacy Pass Routes
Handles legacy pass access, previews, downloads, and benefits
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID
from pathlib import Path

from ...database import get_db
from ...models.member import Member
from ...models.legacy_pass import LegacyPass
from ...models.event import Event
from ...models.payment import Payment
from ...schemas.legacy_pass import (
    LegacyPassPreview,
    LegacyPassFull,
    LegacyPassBenefits,
    LegacyPassDownload
)
from ...api.dependencies import get_current_member
from ...services import (
    validate_legacy_token,
    check_token_payment_status,
    get_legacy_pass_by_token,
    format_pass_number_preview,
    format_gift_list,
    get_gift_categories,
    generate_pass_pdf
)


router = APIRouter(prefix="/legacy-pass", tags=["Legacy Pass"])


@router.get("/preview/{token}", response_model=Dict[str, Any])
async def get_pass_preview(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get blurred preview of legacy pass
    Available before payment is completed
    
    **No Authentication Required** - Uses token only
    
    Shows:
    - Partial pass number
    - Event details
    - Benefits preview (non-personalized)
    - Payment requirement notice
    - Blurred pass images
    
    Args:
        token: Legacy pass token (UUID)
        db: Database session
        
    Returns:
        Blurred pass preview with payment notice
        
    Raises:
        HTTPException 404: If token not found
        HTTPException 400: If token invalid
    """
    # Validate token (don't require payment for preview)
    legacy_pass = validate_legacy_token(db, token)
    
    # Get event details
    event = db.query(Event).filter(Event.id == legacy_pass.event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )
    
    # Get member info
    member = db.query(Member).filter(Member.id == legacy_pass.member_id).first()
    
    # Check payment status
    is_verified, payment = check_token_payment_status(db, token)
    
    # Format partial pass number
    pass_number_preview = format_pass_number_preview(legacy_pass.pass_number)
    
    # Get gift preview
    gift_preview = [
        "Personalized welcome package",
        "Exclusive event merchandise",
        "Premium party favors",
        "Commemorative keepsakes",
        "...and more surprises!"
    ]
    
    # Build preview response
    preview = {
        "token": str(legacy_pass.unique_token),
        "pass_number_partial": pass_number_preview,
        "access_level": legacy_pass.access_level,
        "gift_tier": legacy_pass.gift_tier,
        "event": {
            "name": event.title,
            "date": event.event_date.strftime("%B %d, %Y"),
            "time": event.event_time,
            "venue": event.venue_name
        },
        "benefits_preview": gift_preview,
        "payment": {
            "required": True,
            "amount": 1000.00,
            "currency": "USD",
            "status": payment.status if payment else "pending",
            "is_verified": is_verified
        },
        "blurred_images": {
            "front": f"/static/legacy_passes/{legacy_pass.pass_number.replace('#', '')}_front_blurred.png" if legacy_pass.blurred_preview_path else None,
            "back": f"/static/legacy_passes/{legacy_pass.pass_number.replace('#', '')}_back_blurred.png" if legacy_pass.pass_back_image_path else None
        },
        "message": "Complete your $1,000 investment to unlock full access to your personalized Legacy Pass.",
        "can_access_full": is_verified
    }
    
    return preview


@router.get("/status/{token}", response_model=Dict[str, Any])
async def get_pass_status(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Check payment verification status for a token
    
    **No Authentication Required** - Uses token only
    
    Returns current payment status and whether full pass is accessible
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Payment status and access information
    """
    # Validate token
    legacy_pass = validate_legacy_token(db, token)
    
    # Check payment status
    is_verified, payment = check_token_payment_status(db, token)
    
    if not payment:
        return {
            "token": str(legacy_pass.unique_token),
            "payment_status": "no_payment",
            "is_verified": False,
            "can_access_full_pass": False,
            "message": "No payment record found. Please contact support."
        }
    
    # Build status message
    status_messages = {
        "pending": "Your payment request is being processed. You'll receive full access once verified.",
        "verified": "Payment confirmed! You now have full access to your Legacy Pass.",
        "failed": "Payment verification failed. Please contact our support team."
    }
    
    return {
        "token": str(legacy_pass.unique_token),
        "pass_number": legacy_pass.pass_number,
        "payment_status": payment.status,
        "is_verified": is_verified,
        "can_access_full_pass": is_verified,
        "message": status_messages.get(payment.status, "Payment status unknown."),
        "payment_amount": float(payment.amount),
        "verified_at": payment.verified_at.isoformat() if payment.verified_at else None
    }


@router.get("/full/{token}", response_model=Dict[str, Any])
async def get_full_pass(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get complete legacy pass with all details
    Only accessible after payment verification
    
    **No Authentication Required** - Uses token only
    **Payment Required** - Returns 402 if payment not verified
    
    Returns:
    - Full pass details (unblurred)
    - Complete member information
    - QR code
    - Complete gift list
    - All amenities unlocked
    - Seating information
    - Special perks
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Complete legacy pass information
        
    Raises:
        HTTPException 402: If payment not verified
        HTTPException 404: If token not found
    """
    # Validate token and require payment
    legacy_pass = get_legacy_pass_by_token(db, token, require_payment=True)
    
    # Get member
    member = db.query(Member).filter(Member.id == legacy_pass.member_id).first()
    
    # Get event
    event = db.query(Event).filter(Event.id == legacy_pass.event_id).first()
    
    # Get complete gift list
    gift_list = format_gift_list(legacy_pass.gift_tier)
    
    # Get categorized gifts
    gift_categories = get_gift_categories(legacy_pass.gift_tier)
    
    # Build full pass response
    full_pass = {
        "token": str(legacy_pass.unique_token),
        "pass_number": legacy_pass.pass_number,
        "member": {
            "full_name": member.full_name,
            "email": member.email,
            "membership_tier": member.membership_tier,
            "membership_number": member.membership_number
        },
        "event": {
            "title": event.title,
            "subtitle": event.subtitle,
            "date": event.event_date.strftime("%B %d, %Y"),
            "time": event.event_time,
            "venue_name": event.venue_name,
            "venue_address": event.venue_address,
            "dress_code": event.dress_code
        },
        "access": {
            "level": legacy_pass.access_level,
            "gift_tier": legacy_pass.gift_tier,
            "seating_category": legacy_pass.seating_category or "Premium"
        },
        "qr_code": {
            "data": legacy_pass.qr_code_data,
            "image_url": f"/static/qr_codes/{legacy_pass.pass_number.replace('#', '')}.png" if legacy_pass.qr_code_image_path else None,
            "instructions": "Present this QR code at the event entrance for verification"
        },
        "images": {
            "front_url": f"/static/legacy_passes/{legacy_pass.pass_number.replace('#', '')}_front.png" if legacy_pass.pass_front_image_path else None,
            "back_url": f"/static/legacy_passes/{legacy_pass.pass_number.replace('#', '')}_back.png" if legacy_pass.pass_back_image_path else None
        },
        "gifts": {
            "complete_list": gift_list,
            "by_category": gift_categories,
            "total_items": len(gift_list)
        },
        "amenities": event.amenities if event.amenities else {},
        "special_perks": [
            "Priority event check-in",
            "VIP seating assignment",
            "Complimentary valet parking",
            "Access to exclusive lounge",
            "Professional photography included",
            "Commemorative gift package"
        ],
        "message": "Welcome to the Inner Circle. This pass is your key to an unforgettable evening.",
        "is_transferable": False,
        "valid_until": event.event_date.isoformat()
    }
    
    return full_pass


@router.get("/download/{token}", response_model=LegacyPassDownload)
async def get_download_urls(
    token: str,
    db: Session = Depends(get_db)
) -> LegacyPassDownload:
    """
    Get download URLs for legacy pass files
    Payment verification required
    
    **No Authentication Required** - Uses token only
    **Payment Required**
    
    Returns URLs for:
    - PDF version
    - Front image (PNG)
    - Back image (PNG)
    - Apple Wallet (if available)
    - Google Wallet (if available)
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Download URLs
        
    Raises:
        HTTPException 402: If payment not verified
    """
    # Validate token and require payment
    legacy_pass = get_legacy_pass_by_token(db, token, require_payment=True)
    
    # Generate PDF if not exists
    if not legacy_pass.full_pass_pdf_path:
        try:
            member = db.query(Member).filter(Member.id == legacy_pass.member_id).first()
            pdf_path = generate_pass_pdf(
                front_path=legacy_pass.pass_front_image_path,
                back_path=legacy_pass.pass_back_image_path,
                pass_number=legacy_pass.pass_number,
                member_name=member.full_name
            )
            legacy_pass.full_pass_pdf_path = pdf_path
            db.commit()
        except Exception as e:
            print(f"Warning: PDF generation failed: {e}")
    
    # Build download URLs
    base_filename = legacy_pass.pass_number.replace('#', '')
    
    return LegacyPassDownload(
        pdf_url=f"/static/legacy_passes/pdf/{base_filename}.pdf" if legacy_pass.full_pass_pdf_path else None,
        front_image_url=f"/static/legacy_passes/{base_filename}_front.png" if legacy_pass.pass_front_image_path else None,
        back_image_url=f"/static/legacy_passes/{base_filename}_back.png" if legacy_pass.pass_back_image_path else None,
        apple_wallet_url=None,  # Not implemented yet
        google_wallet_url=None  # Not implemented yet
    )


@router.get("/download/{token}/pdf")
async def download_pass_pdf(
    token: str,
    db: Session = Depends(get_db)
) -> FileResponse:
    """
    Download legacy pass as PDF file
    Payment verification required
    
    **No Authentication Required** - Uses token only
    **Payment Required**
    
    Triggers file download in browser
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        PDF file download
        
    Raises:
        HTTPException 402: If payment not verified
        HTTPException 404: If PDF not found
    """
    # Validate token and require payment
    legacy_pass = get_legacy_pass_by_token(db, token, require_payment=True)
    
    # Check if PDF exists
    if not legacy_pass.full_pass_pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not yet generated. Please try again in a moment."
        )
    
    # Check file exists
    pdf_path = Path(legacy_pass.full_pass_pdf_path)
    if not pdf_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found on server."
        )
    
    # Return file download
    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"Legacy_Pass_{legacy_pass.pass_number.replace('#', '')}.pdf"
    )


@router.get("/benefits/{token}", response_model=Dict[str, Any])
async def get_pass_benefits(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get complete list of benefits unlocked by legacy pass
    Payment verification required
    
    **No Authentication Required** - Uses token only
    **Payment Required**
    
    Returns:
    - Gift tier and complete gift list
    - Amenities access
    - Seating category
    - Special perks
    - Raffle entries
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Complete benefits information
        
    Raises:
        HTTPException 402: If payment not verified
    """
    # Validate token and require payment
    legacy_pass = get_legacy_pass_by_token(db, token, require_payment=True)
    
    # Get event
    event = db.query(Event).filter(Event.id == legacy_pass.event_id).first()
    
    # Get complete gift list
    gift_list = format_gift_list(legacy_pass.gift_tier)
    gift_categories = get_gift_categories(legacy_pass.gift_tier)
    
    # Raffle entries by tier
    raffle_entries = {
        "standard": 2,
        "premium": 5,
        "elite": 10
    }
    
    # Build benefits response
    benefits = {
        "access_level": legacy_pass.access_level,
        "gift_tier": legacy_pass.gift_tier,
        "gifts": {
            "total_items": len(gift_list),
            "complete_list": gift_list,
            "by_category": gift_categories
        },
        "amenities": {
            "all_amenities": event.amenities if event.amenities else {},
            "description": "Full access to all luxury amenities and services"
        },
        "seating": {
            "category": legacy_pass.seating_category or "Premium",
            "priority": "Priority seating in exclusive section"
        },
        "raffle": {
            "entries": raffle_entries.get(legacy_pass.gift_tier, 1),
            "description": "Entries for exclusive prize drawings"
        },
        "special_perks": [
            "Priority check-in at event",
            "Complimentary valet parking",
            "Access to VIP lounge",
            "Professional photography session",
            "Commemorative certificate",
            "Early access to future events",
            "Exclusive member merchandise"
        ],
        "message": f"As a {legacy_pass.gift_tier.title()} tier member, you have access to an exceptional experience."
    }
    
    return benefits


@router.get("/verify/{token}", response_model=Dict[str, Any])
async def verify_pass_at_event(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Verify legacy pass at event entrance
    Used by event staff to validate passes
    
    **No Authentication Required** - Uses token only
    
    Returns validation status and member information
    
    Args:
        token: Legacy pass token (from QR code scan)
        db: Database session
        
    Returns:
        Verification result with member info
    """
    try:
        # Validate token
        legacy_pass = validate_legacy_token(db, token)
        
        # Check payment
        is_verified, payment = check_token_payment_status(db, token)
        
        if not is_verified:
            return {
                "valid": False,
                "reason": "payment_not_verified",
                "message": "Payment has not been verified. Please see registration desk."
            }
        
        # Get member
        member = db.query(Member).filter(Member.id == legacy_pass.member_id).first()
        
        # Get event
        event = db.query(Event).filter(Event.id == legacy_pass.event_id).first()
        
        return {
            "valid": True,
            "pass_number": legacy_pass.pass_number,
            "member_name": member.full_name,
            "membership_tier": member.membership_tier,
            "access_level": legacy_pass.access_level,
            "seating_category": legacy_pass.seating_category,
            "event_name": event.title,
            "message": f"Welcome, {member.full_name}! Enjoy the evening."
        }
        
    except HTTPException:
        return {
            "valid": False,
            "reason": "invalid_token",
            "message": "This pass could not be verified. Please see registration desk."
        }