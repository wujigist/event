"""
Token Service
Manages unique tokens for legacy pass access and validation
"""

import uuid
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.legacy_pass import LegacyPass
from ..models.payment import Payment


def generate_unique_token() -> uuid.UUID:
    """
    Generate a unique UUID token for legacy pass access
    
    Returns:
        UUID token
    """
    return uuid.uuid4()


def validate_legacy_token(db: Session, token: str) -> Optional[LegacyPass]:
    """
    Validate if a legacy pass token exists and is active
    
    Args:
        db: Database session
        token: Token string (UUID format)
        
    Returns:
        LegacyPass object if valid, None otherwise
        
    Raises:
        HTTPException: If token is invalid or pass is inactive
    """
    try:
        # Convert string to UUID
        token_uuid = uuid.UUID(token)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format. Please check your invitation."
        )
    
    # Query legacy pass by token
    legacy_pass = db.query(LegacyPass).filter(
        LegacyPass.unique_token == token_uuid,
        LegacyPass.is_active == True
    ).first()
    
    if not legacy_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This invitation could not be found or has been deactivated."
        )
    
    return legacy_pass


def check_token_payment_status(db: Session, token: str) -> Tuple[bool, Optional[Payment]]:
    """
    Verify if payment has been completed for a legacy pass token
    
    Args:
        db: Database session
        token: Legacy pass token
        
    Returns:
        Tuple of (is_verified: bool, payment: Payment or None)
    """
    # Validate token first
    legacy_pass = validate_legacy_token(db, token)
    
    # Get payment record
    payment = db.query(Payment).filter(
        Payment.legacy_pass_id == legacy_pass.id
    ).first()
    
    if not payment:
        return False, None
    
    # Check if payment is verified
    is_verified = payment.status == "verified"
    
    return is_verified, payment


def get_legacy_pass_by_token(db: Session, token: str, require_payment: bool = False) -> LegacyPass:
    """
    Get legacy pass by token with optional payment verification
    
    Args:
        db: Database session
        token: Legacy pass token
        require_payment: If True, requires payment to be verified
        
    Returns:
        LegacyPass object
        
    Raises:
        HTTPException: If token invalid or payment not verified (when required)
    """
    # Validate token
    legacy_pass = validate_legacy_token(db, token)
    
    # Check payment if required
    if require_payment:
        is_verified, payment = check_token_payment_status(db, str(token))
        
        if not is_verified:
            payment_status = payment.status if payment else "pending"
            
            if payment_status == "pending":
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Your $1,000 investment is required to unlock full access to your Legacy Pass. Please complete the payment process."
                )
            elif payment_status == "failed":
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Payment verification failed. Please contact our support team for assistance."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Payment processing in progress. You'll receive full access once verified."
                )
    
    return legacy_pass


def format_pass_number_preview(pass_number: str) -> str:
    """
    Create a partially obscured version of pass number for preview
    
    Args:
        pass_number: Full pass number (e.g., "INNER-CIRCLE-#001")
        
    Returns:
        Partially hidden pass number (e.g., "INNER-CIRCLE-#***")
    """
    # Split pass number to hide the last part
    parts = pass_number.split("#")
    if len(parts) == 2:
        return f"{parts[0]}#***"
    return "***"


def get_token_access_level(db: Session, token: str) -> dict:
    """
    Get access level information for a token
    
    Args:
        db: Database session
        token: Legacy pass token
        
    Returns:
        Dictionary with access level info
    """
    legacy_pass = validate_legacy_token(db, token)
    is_verified, payment = check_token_payment_status(db, token)
    
    return {
        "token": str(legacy_pass.unique_token),
        "pass_number": legacy_pass.pass_number,
        "access_level": legacy_pass.access_level,
        "gift_tier": legacy_pass.gift_tier,
        "has_payment": payment is not None,
        "payment_verified": is_verified,
        "can_access_full_pass": is_verified,
        "payment_status": payment.status if payment else "no_payment"
    }


def deactivate_legacy_pass(db: Session, token: str, reason: str = None) -> bool:
    """
    Deactivate a legacy pass (admin function)
    
    Args:
        db: Database session
        token: Legacy pass token
        reason: Optional reason for deactivation
        
    Returns:
        True if successful
    """
    legacy_pass = validate_legacy_token(db, token)
    
    legacy_pass.is_active = False
    db.commit()
    
    return True


def reactivate_legacy_pass(db: Session, token: str) -> bool:
    """
    Reactivate a legacy pass (admin function)
    
    Args:
        db: Database session
        token: Legacy pass token
        
    Returns:
        True if successful
    """
    try:
        token_uuid = uuid.UUID(token)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format"
        )
    
    legacy_pass = db.query(LegacyPass).filter(
        LegacyPass.unique_token == token_uuid
    ).first()
    
    if not legacy_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legacy pass not found"
        )
    
    legacy_pass.is_active = True
    db.commit()
    
    return True