"""
Authentication Routes
Handles member authentication, login, and session management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from ...database import get_db
from ...models.member import Member
from ...schemas.member import MemberLogin, TokenResponse, MemberResponse
from ...services.auth_service import (
    authenticate_member,
    logout_member,
    get_current_member
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/request-access", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def request_access(
    credentials: MemberLogin,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Request access to the Inner Circle experience
    Validates email and generates access token if member exists
    
    **This is the primary authentication endpoint**
    
    Args:
        credentials: Member email credentials
        db: Database session
        
    Returns:
        Access token and member information
        
    Raises:
        HTTPException 404: If email not found in members list
    """
    # Authenticate member
    auth_result = authenticate_member(db, credentials.email)
    
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This invitation is reserved for selected members. If you believe this is an error, please contact our support team."
        )
    
    # Extract data
    access_token = auth_result["access_token"]
    token_type = auth_result["token_type"]
    member = auth_result["member"]
    
    # Create response
    return TokenResponse(
        access_token=access_token,
        token_type=token_type,
        member=MemberResponse.model_validate(member)
    )


@router.get("/me", response_model=MemberResponse)
async def get_current_user(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> MemberResponse:
    """
    Get current authenticated member information
    Used to maintain session and verify authentication
    
    **Protected Route** - Requires valid JWT token
    
    Args:
        current_member: Authenticated member from dependency
        db: Database session
        
    Returns:
        Current member details
    """
    # Refresh member data from database
    db.refresh(current_member)
    
    return MemberResponse.model_validate(current_member)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Logout current member
    Clears session token from database
    
    **Protected Route** - Requires valid JWT token
    
    Args:
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Success message
    """
    # Clear member session
    logout_member(db, current_member)
    
    return {
        "message": "You have been successfully logged out. We look forward to welcoming you back soon.",
        "status": "success"
    }


@router.post("/verify-token", response_model=Dict[str, Any])
async def verify_token(
    current_member: Member = Depends(get_current_member)
) -> Dict[str, Any]:
    """
    Verify if current token is valid
    Useful for frontend to check authentication status
    
    **Protected Route** - Requires valid JWT token
    
    Args:
        current_member: Authenticated member
        
    Returns:
        Verification status and member info
    """
    return {
        "valid": True,
        "member_id": str(current_member.id),
        "email": current_member.email,
        "full_name": current_member.full_name,
        "membership_tier": current_member.membership_tier,
        "has_logged_in": current_member.has_logged_in
    }


@router.get("/status", response_model=Dict[str, Any])
async def auth_status() -> Dict[str, Any]:
    """
    Check authentication system status
    Public endpoint for health checks
    
    Returns:
        System status
    """
    return {
        "status": "operational",
        "authentication": "active",
        "message": "Authentication system is ready to welcome you."
    }