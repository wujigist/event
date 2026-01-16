"""
RSVP Routes
Handles event RSVP submissions (accept/decline) and status checking
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID
from datetime import datetime

from ...database import get_db
from ...models.member import Member
from ...models.event import Event
from ...models.rsvp import RSVP
from ...models.legacy_pass import LegacyPass
from ...models.payment import Payment
from ...schemas.rsvp import (
    RSVPCreate,
    RSVPResponse,
    RSVPAcceptedResponse,
    RSVPDeclinedResponse,
    RSVPStatusResponse
)
from ...api.dependencies import get_current_member
from ...services import (
    generate_unique_token,
    save_qr_code_image,
    save_pass_assets,
    assign_gift_tier,
    send_rsvp_confirmation,
    send_decline_thank_you
)


router = APIRouter(prefix="/rsvp", tags=["RSVP"])


@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def submit_rsvp(
    rsvp_data: RSVPCreate,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Submit RSVP for an event (Accept or Decline)
    
    **Protected Route** - Requires authentication
    
    **On Accept:**
    - Creates RSVP record
    - Generates unique Legacy Pass token
    - Creates Legacy Pass record
    - Generates QR code
    - Creates blurred pass preview
    - Creates Payment record (pending)
    - Sends confirmation email
    - Returns token and next steps
    
    **On Decline:**
    - Creates RSVP record
    - Sends thank you email
    - Returns graceful message
    
    Args:
        rsvp_data: RSVP submission with event_id and status
        current_member: Authenticated member
        db: Database session
        
    Returns:
        RSVP response with appropriate next steps
        
    Raises:
        HTTPException 404: If event not found
        HTTPException 400: If RSVP already exists or invalid status
    """
    # Validate event exists
    event = db.query(Event).filter(
        Event.id == rsvp_data.event_id,
        Event.is_active == True
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This event could not be found or is no longer active."
        )
    
    # Check if RSVP already exists
    existing_rsvp = db.query(RSVP).filter(
        RSVP.member_id == current_member.id,
        RSVP.event_id == rsvp_data.event_id
    ).first()
    
    if existing_rsvp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already responded to this invitation. To change your response, please contact our support team."
        )
    
    # Validate status
    if rsvp_data.status.lower() not in ["accepted", "declined"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RSVP status must be either 'accepted' or 'declined'."
        )
    
    # Create RSVP record
    rsvp = RSVP(
        member_id=current_member.id,
        event_id=rsvp_data.event_id,
        status=rsvp_data.status.lower(),
        response_message=rsvp_data.response_message,
        responded_at=datetime.utcnow()
    )
    
    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)
    
    # Handle ACCEPTED response
    if rsvp.status == "accepted":
        # Generate unique token
        unique_token = generate_unique_token()
        
        # Generate pass number
        # Format: INNER-CIRCLE-#XXX
        member_count = db.query(LegacyPass).count()
        pass_number = f"INNER-CIRCLE-#{str(member_count + 1).zfill(3)}"
        
        # Assign gift tier based on membership
        gift_tier = assign_gift_tier(current_member.membership_tier)
        
        # Determine access level
        access_level_map = {
            "founding_member": "diamond",
            "vip": "platinum",
            "inner_circle": "gold"
        }
        access_level = access_level_map.get(
            current_member.membership_tier.lower(),
            "gold"
        )
        
        # Create Legacy Pass
        legacy_pass = LegacyPass(
            member_id=current_member.id,
            event_id=event.id,
            pass_number=pass_number,
            unique_token=unique_token,
            access_level=access_level,
            gift_tier=gift_tier,
            seating_category="VIP" if current_member.membership_tier != "inner_circle" else "Premium"
        )
        
        db.add(legacy_pass)
        db.commit()
        db.refresh(legacy_pass)
        
        # Generate QR code
        try:
            qr_result = save_qr_code_image(
                pass_number=pass_number,
                member_name=current_member.full_name,
                event_id=str(event.id),
                token=str(unique_token),
                event_date=event.event_date.strftime("%B %d, %Y")
            )
            
            # Update legacy pass with QR code info
            legacy_pass.qr_code_data = qr_result["qr_data"]
            legacy_pass.qr_code_image_path = qr_result["qr_image_path"]
            
        except Exception as e:
            print(f"Warning: QR code generation failed: {e}")
            # Continue anyway - QR code is not critical for RSVP
        
        # Generate pass images (blurred preview)
        try:
            pass_assets = save_pass_assets(
                member_name=current_member.full_name,
                pass_number=pass_number,
                membership_tier=current_member.membership_tier,
                event_name=event.title,
                event_date=event.event_date.strftime("%B %d, %Y"),
                venue_name=event.venue_name,
                token=str(unique_token),
                qr_code_path=legacy_pass.qr_code_image_path or ""
            )
            
            # Update legacy pass with asset paths
            legacy_pass.pass_front_image_path = pass_assets["front_path"]
            legacy_pass.pass_back_image_path = pass_assets["back_path"]
            legacy_pass.blurred_preview_path = pass_assets["front_blurred_path"]
            
        except Exception as e:
            print(f"Warning: Pass generation failed: {e}")
            # Continue anyway - passes can be regenerated later
        
        db.commit()
        
        # Create Payment record (pending)
        payment = Payment(
            member_id=current_member.id,
            legacy_pass_id=legacy_pass.id,
            amount=1000.00,
            currency="USD",
            contact_email=current_member.email,
            status="pending"
        )
        
        db.add(payment)
        db.commit()
        
        # Send confirmation email
        try:
            await send_rsvp_confirmation(
                to_email=current_member.email,
                member_name=current_member.full_name,
                token=str(unique_token)
            )
        except Exception as e:
            print(f"Warning: Email sending failed: {e}")
            # Continue anyway - email is not critical
        
        # Return acceptance response
        return {
            "status": "success",
            "message": "I can't wait to share this moment with you. - Paige",
            "rsvp": RSVPResponse.model_validate(rsvp),
            "legacy_token": str(unique_token),
            "pass_number": pass_number,
            "gift_tier": gift_tier,
            "access_level": access_level,
            "payment_required": True,
            "payment_amount": 1000.00,
            "next_steps": "Complete your $1,000 investment to unlock full access to your Legacy Pass and all exclusive benefits.",
            "pass_preview_available": True
        }
    
    # Handle DECLINED response
    else:
        # Send thank you email
        try:
            await send_decline_thank_you(
                to_email=current_member.email,
                member_name=current_member.full_name
            )
        except Exception as e:
            print(f"Warning: Email sending failed: {e}")
        
        # Return decline response
        return {
            "status": "success",
            "message": "While I'm saddened you won't be able to join us, I completely understand. You'll remain in my thoughts throughout the evening.",
            "rsvp": RSVPResponse.model_validate(rsvp),
            "appreciation_message": "Thank you for being part of my Inner Circle. You'll have priority access to all future exclusive events.",
            "future_access": True
        }


@router.get("/status", response_model=RSVPStatusResponse)
async def get_rsvp_status(
    event_id: UUID = None,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> RSVPStatusResponse:
    """
    Get current member's RSVP status
    
    **Protected Route** - Requires authentication
    
    If event_id provided, checks RSVP for that specific event.
    Otherwise, checks for any active event RSVP.
    
    Args:
        event_id: Optional event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        RSVP status information
    """
    # If no event_id, get current active event
    if not event_id:
        event = db.query(Event).filter(Event.is_active == True).first()
        if not event:
            return RSVPStatusResponse(
                has_rsvp=False,
                status=None,
                rsvp=None
            )
        event_id = event.id
    
    # Check for RSVP
    rsvp = db.query(RSVP).filter(
        RSVP.member_id == current_member.id,
        RSVP.event_id == event_id
    ).first()
    
    if not rsvp:
        return RSVPStatusResponse(
            has_rsvp=False,
            status=None,
            rsvp=None
        )
    
    return RSVPStatusResponse(
        has_rsvp=True,
        status=rsvp.status,
        rsvp=RSVPResponse.model_validate(rsvp)
    )


@router.get("/me", response_model=Dict[str, Any])
async def get_my_rsvp(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current member's RSVP details with full context
    
    **Protected Route** - Requires authentication
    
    Returns RSVP information along with:
    - Event details
    - Legacy pass token (if accepted)
    - Payment status (if accepted)
    - Next steps
    
    Args:
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Complete RSVP context
    """
    # Get current active event
    event = db.query(Event).filter(Event.is_active == True).first()
    
    if not event:
        return {
            "has_active_event": False,
            "message": "No active event at this time."
        }
    
    # Check for RSVP
    rsvp = db.query(RSVP).filter(
        RSVP.member_id == current_member.id,
        RSVP.event_id == event.id
    ).first()
    
    if not rsvp:
        return {
            "has_active_event": True,
            "event_id": str(event.id),
            "event_title": event.title,
            "event_date": event.event_date.strftime("%B %d, %Y"),
            "has_rsvp": False,
            "message": "You haven't responded to this invitation yet."
        }
    
    response_data = {
        "has_active_event": True,
        "event_id": str(event.id),
        "event_title": event.title,
        "event_date": event.event_date.strftime("%B %d, %Y"),
        "has_rsvp": True,
        "rsvp_status": rsvp.status,
        "responded_at": rsvp.responded_at.isoformat()
    }
    
    # If accepted, include legacy pass info
    if rsvp.status == "accepted":
        legacy_pass = db.query(LegacyPass).filter(
            LegacyPass.member_id == current_member.id,
            LegacyPass.event_id == event.id
        ).first()
        
        if legacy_pass:
            # Check payment status
            payment = db.query(Payment).filter(
                Payment.legacy_pass_id == legacy_pass.id
            ).first()
            
            response_data.update({
                "legacy_pass_token": str(legacy_pass.unique_token),
                "pass_number": legacy_pass.pass_number,
                "access_level": legacy_pass.access_level,
                "gift_tier": legacy_pass.gift_tier,
                "payment_status": payment.status if payment else "no_payment",
                "payment_required": payment.status != "verified" if payment else True,
                "can_access_full_pass": payment.status == "verified" if payment else False
            })
    
    return response_data


@router.delete("/{rsvp_id}", status_code=status.HTTP_200_OK)
async def cancel_rsvp(
    rsvp_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Cancel an RSVP (admin or member self-cancel)
    
    **Protected Route** - Requires authentication
    
    Note: In production, you may want to restrict this to admin only
    or have specific cancellation policies.
    
    Args:
        rsvp_id: RSVP UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 404: If RSVP not found
        HTTPException 403: If not authorized
    """
    # Get RSVP
    rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    
    if not rsvp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSVP not found."
        )
    
    # Check authorization
    if rsvp.member_id != current_member.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own RSVP."
        )
    
    # Delete RSVP
    db.delete(rsvp)
    db.commit()
    
    return {
        "message": "Your RSVP has been cancelled. If you'd like to reconsider, please contact our support team.",
        "status": "success"
    }