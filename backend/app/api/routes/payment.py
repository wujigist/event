"""
Payment Routes
Handles payment methods, contact submission, and status checking
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime

from ...database import get_db
from ...models.member import Member
from ...models.payment import Payment
from ...models.legacy_pass import LegacyPass
from ...schemas.payment import (
    PaymentMethodResponse,
    PaymentContactSubmit,
    PaymentContactResponse,
    PaymentStatusResponse,
    PaymentVerify,
    PaymentVerifiedResponse
)
from ...api.dependencies import get_current_member, require_admin
from ...services import (
    validate_legacy_token,
    send_payment_instructions,
    send_payment_verified,
    notify_admin_payment_request
)


router = APIRouter(prefix="/payment", tags=["Payment"])


@router.get("/methods", response_model=PaymentMethodResponse)
async def get_payment_methods() -> PaymentMethodResponse:
    """
    Get available payment methods
    
    **Public Endpoint** - No authentication required
    
    Returns list of accepted payment methods with descriptions
    
    Returns:
        Available payment methods
    """
    methods = [
        {
            "id": "bank_transfer",
            "name": "Bank Transfer",
            "description": "Direct bank transfer (ACH or wire)",
            "processing_time": "1-3 business days",
            "icon": "🏦"
        },
        {
            "id": "credit_card",
            "name": "Credit/Debit Card",
            "description": "Visa, Mastercard, American Express",
            "processing_time": "Instant verification",
            "icon": "💳"
        },
        {
            "id": "paypal",
            "name": "PayPal",
            "description": "Secure PayPal payment",
            "processing_time": "Instant verification",
            "icon": "💰"
        },
        {
            "id": "cryptocurrency",
            "name": "Cryptocurrency",
            "description": "Bitcoin, Ethereum, USDC",
            "processing_time": "1-2 hours for confirmation",
            "icon": "₿"
        },
        {
            "id": "wire_transfer",
            "name": "Wire Transfer",
            "description": "International wire transfer",
            "processing_time": "2-5 business days",
            "icon": "🌐"
        },
        {
            "id": "other",
            "name": "Other",
            "description": "Zelle, Venmo, or alternative methods",
            "processing_time": "Varies",
            "icon": "📱"
        }
    ]
    
    return PaymentMethodResponse(methods=methods)


@router.post("/contact", response_model=PaymentContactResponse)
async def submit_payment_contact(
    payment_data: PaymentContactSubmit,
    db: Session = Depends(get_db)
) -> PaymentContactResponse:
    """
    Submit contact information for payment
    Member provides email and selected payment method
    
    **No Authentication Required** - Uses legacy pass token only
    
    Process:
    1. Validates legacy pass token
    2. Updates payment record with contact info
    3. Sends confirmation email to member
    4. Notifies admin of payment request
    5. Admin will contact member within 24 hours
    
    Args:
        payment_data: Payment contact submission
        db: Database session
        
    Returns:
        Confirmation with next steps
        
    Raises:
        HTTPException 404: If token or payment not found
        HTTPException 400: If payment already verified
    """
    # Validate legacy pass token
    legacy_pass = validate_legacy_token(db, str(payment_data.legacy_token))
    
    # Get payment record
    payment = db.query(Payment).filter(
        Payment.legacy_pass_id == legacy_pass.id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment record not found. Please contact support."
        )
    
    # Check if already verified
    if payment.status == "verified":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment has already been verified. You have full access to your Legacy Pass."
        )
    
    # Update payment record
    payment.contact_email = payment_data.contact_email
    payment.payment_method = payment_data.payment_method
    payment.status = "pending"
    payment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(payment)
    
    # Get member info
    member = db.query(Member).filter(Member.id == legacy_pass.member_id).first()
    
    # Send confirmation email to member
    try:
        await send_payment_instructions(
            to_email=payment_data.contact_email,
            member_name=member.full_name,
            payment_method=payment_data.payment_method,
            contact_email=payment_data.contact_email
        )
    except Exception as e:
        print(f"Warning: Email to member failed: {e}")
    
    # Notify admin
    try:
        # In production, you'd have an admin email in settings
        admin_email = "admin@paigeinnercircle.com"
        await notify_admin_payment_request(
            admin_email=admin_email,
            member_name=member.full_name,
            member_email=member.email,
            payment_method=payment_data.payment_method,
            contact_email=payment_data.contact_email,
            pass_number=legacy_pass.pass_number
        )
    except Exception as e:
        print(f"Warning: Admin notification failed: {e}")
    
    return PaymentContactResponse(
        message="Thank you! Your payment request has been received.",
        status="pending",
        next_steps="Our team will contact you at the provided email within 24 hours with payment instructions.",
        estimated_contact_time="Within 24 hours"
    )


@router.get("/status/{token}", response_model=PaymentStatusResponse)
async def get_payment_status(
    token: str,
    db: Session = Depends(get_db)
) -> PaymentStatusResponse:
    """
    Check payment verification status
    
    **No Authentication Required** - Uses legacy pass token only
    
    Returns current payment status and whether member can access full pass
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Payment status information
        
    Raises:
        HTTPException 404: If token or payment not found
    """
    # Validate legacy pass token
    legacy_pass = validate_legacy_token(db, token)
    
    # Get payment record
    payment = db.query(Payment).filter(
        Payment.legacy_pass_id == legacy_pass.id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment record not found."
        )
    
    # Determine if verified
    is_verified = payment.status == "verified"
    
    # Status messages
    status_messages = {
        "pending": "Your payment request is being processed. You'll receive an update within 24 hours.",
        "verified": "Payment confirmed! You now have full access to your Legacy Pass.",
        "failed": "Payment verification encountered an issue. Our team will contact you shortly."
    }
    
    return PaymentStatusResponse(
        payment_id=payment.id,
        status=payment.status,
        is_verified=is_verified,
        verified_at=payment.verified_at,
        can_access_full_pass=is_verified,
        message=status_messages.get(payment.status, "Payment status unknown.")
    )


@router.post("/verify", response_model=PaymentVerifiedResponse)
async def verify_payment(
    verification: PaymentVerify,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> PaymentVerifiedResponse:
    """
    Verify a payment (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Process:
    1. Marks payment as verified
    2. Records admin who verified
    3. Sends confirmation email to member
    4. Member gains full access to Legacy Pass
    
    Args:
        verification: Payment verification data
        current_admin: Authenticated admin user
        db: Database session
        
    Returns:
        Verification confirmation
        
    Raises:
        HTTPException 404: If payment not found
        HTTPException 400: If already verified
    """
    # Get payment
    payment = db.query(Payment).filter(
        Payment.id == verification.payment_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment record not found."
        )
    
    # Check if already verified
    if payment.status == "verified":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment has already been verified."
        )
    
    # Update payment
    payment.status = "verified"
    payment.verified_by = verification.verified_by
    payment.verified_at = datetime.utcnow()
    payment.notes = verification.notes
    payment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(payment)
    
    # Get legacy pass and member
    legacy_pass = db.query(LegacyPass).filter(
        LegacyPass.id == payment.legacy_pass_id
    ).first()
    
    member = db.query(Member).filter(
        Member.id == payment.member_id
    ).first()
    
    # Send confirmation email to member
    try:
        await send_payment_verified(
            to_email=member.email,
            member_name=member.full_name,
            pass_token=str(legacy_pass.unique_token)
        )
    except Exception as e:
        print(f"Warning: Verification email failed: {e}")
    
    return PaymentVerifiedResponse(
        message=f"Payment verified successfully. {member.full_name} now has full access.",
        payment=payment,
        full_pass_access_granted=True
    )


@router.get("/admin/pending")
async def get_pending_payments(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get all pending payment requests (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Returns list of payments awaiting verification
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        List of pending payments with member and pass info
    """
    # Get all pending payments
    pending_payments = db.query(Payment).filter(
        Payment.status == "pending"
    ).order_by(Payment.created_at.desc()).all()
    
    result = []
    
    for payment in pending_payments:
        # Get member
        member = db.query(Member).filter(
            Member.id == payment.member_id
        ).first()
        
        # Get legacy pass
        legacy_pass = db.query(LegacyPass).filter(
            LegacyPass.id == payment.legacy_pass_id
        ).first()
        
        result.append({
            "payment_id": str(payment.id),
            "member": {
                "name": member.full_name,
                "email": member.email,
                "tier": member.membership_tier
            },
            "pass_number": legacy_pass.pass_number if legacy_pass else None,
            "amount": float(payment.amount),
            "payment_method": payment.payment_method,
            "contact_email": payment.contact_email,
            "submitted_at": payment.created_at.isoformat(),
            "days_pending": (datetime.utcnow() - payment.created_at).days
        })
    
    return result


@router.get("/admin/all")
async def get_all_payments(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db),
    status_filter: str = None
) -> List[Dict[str, Any]]:
    """
    Get all payment records (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Optional filter by status
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        status_filter: Optional status filter (pending, verified, failed)
        
    Returns:
        List of all payments
    """
    # Build query
    query = db.query(Payment).order_by(Payment.created_at.desc())
    
    if status_filter:
        query = query.filter(Payment.status == status_filter)
    
    payments = query.all()
    
    result = []
    
    for payment in payments:
        member = db.query(Member).filter(Member.id == payment.member_id).first()
        legacy_pass = db.query(LegacyPass).filter(
            LegacyPass.id == payment.legacy_pass_id
        ).first()
        
        result.append({
            "payment_id": str(payment.id),
            "status": payment.status,
            "member_name": member.full_name if member else "Unknown",
            "member_email": member.email if member else "Unknown",
            "pass_number": legacy_pass.pass_number if legacy_pass else None,
            "amount": float(payment.amount),
            "payment_method": payment.payment_method,
            "contact_email": payment.contact_email,
            "submitted_at": payment.created_at.isoformat(),
            "verified_at": payment.verified_at.isoformat() if payment.verified_at else None,
            "verified_by": payment.verified_by,
            "notes": payment.notes
        })
    
    return result


@router.put("/{payment_id}/status")
async def update_payment_status(
    payment_id: UUID,
    new_status: str,
    notes: str = None,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update payment status (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Can be used to mark as failed or make other status updates
    
    Args:
        payment_id: Payment UUID
        new_status: New status (pending, verified, failed)
        notes: Optional admin notes
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Updated payment status
        
    Raises:
        HTTPException 404: If payment not found
        HTTPException 400: If invalid status
    """
    # Validate status
    valid_statuses = ["pending", "verified", "failed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Get payment
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )
    
    # Update status
    payment.status = new_status
    payment.updated_at = datetime.utcnow()
    
    if notes:
        payment.notes = notes
    
    if new_status == "verified":
        payment.verified_by = current_admin.email
        payment.verified_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Payment status updated to {new_status}",
        "payment_id": str(payment.id),
        "status": payment.status,
        "updated_at": payment.updated_at.isoformat()
    }