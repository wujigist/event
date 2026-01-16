"""
Authentication Service
Handles member authentication, JWT token generation, and session management
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..config import settings
from ..models.member import Member
from ..database import get_db

# Security scheme for Bearer token
security = HTTPBearer()


def validate_member_email(db: Session, email: str) -> Optional[Member]:
    """
    Check if email exists in the members database
    
    Args:
        db: Database session
        email: Member email address
        
    Returns:
        Member object if found, None otherwise
    """
    member = db.query(Member).filter(
        Member.email == email,
        Member.is_active == True
    ).first()
    
    return member


def generate_access_token(member_id: str, email: str) -> dict:
    """
    Create JWT access token for member session
    
    Args:
        member_id: Member UUID as string
        email: Member email
        
    Returns:
        Dictionary with access_token and token_type
    """
    # Calculate expiration time
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    # Create payload
    payload = {
        "sub": str(member_id),  # Subject (member ID)
        "email": email,
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access"
    }
    
    # Encode JWT token
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expires_at": expire
    }


def verify_access_token(token: str) -> dict:
    """
    Validate and decode JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please access your invitation again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract member ID
        member_id: str = payload.get("sub")
        if member_id is None:
            raise credentials_exception
            
        return payload
        
    except JWTError:
        raise credentials_exception


def create_member_session(db: Session, member: Member, token_data: dict) -> Member:
    """
    Store session information in member record
    
    Args:
        db: Database session
        member: Member object
        token_data: Token data including access_token and expires_at
        
    Returns:
        Updated member object
    """
    # Update member with session info
    member.access_token = token_data["access_token"]
    member.token_expires_at = token_data["expires_at"]
    member.has_logged_in = True
    member.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(member)
    
    return member


def get_current_member(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Member:
    """
    Dependency to get current authenticated member
    Used in protected routes to ensure user is authenticated
    
    Args:
        credentials: HTTP Bearer credentials from request header
        db: Database session
        
    Returns:
        Current authenticated member
        
    Raises:
        HTTPException: If authentication fails
    """
    # Verify token
    payload = verify_access_token(credentials.credentials)
    member_id = payload.get("sub")
    
    # Get member from database
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This invitation could not be found. Please contact support.",
        )
    
    if not member.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your access has been revoked. Please contact support.",
        )
    
    return member


def authenticate_member(db: Session, email: str) -> Optional[dict]:
    """
    Complete authentication flow for a member
    
    Args:
        db: Database session
        email: Member email
        
    Returns:
        Dictionary with token and member info, or None if not found
    """
    # Validate email exists
    member = validate_member_email(db, email)
    
    if not member:
        return None
    
    # Generate token
    token_data = generate_access_token(str(member.id), member.email)
    
    # Create session
    member = create_member_session(db, member, token_data)
    
    return {
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"],
        "member": member
    }


def logout_member(db: Session, member: Member) -> bool:
    """
    Clear member session (optional implementation)
    
    Args:
        db: Database session
        member: Member object
        
    Returns:
        True if successful
    """
    member.access_token = None
    member.token_expires_at = None
    member.updated_at = datetime.utcnow()
    
    db.commit()
    
    return True