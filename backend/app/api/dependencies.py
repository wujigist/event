"""
API Dependencies
Common dependencies used across API routes
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db as get_database_session
from ..models.member import Member
from ..services.auth_service import get_current_member as get_authenticated_member


# Re-export database dependency for convenience
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    Provides a SQLAlchemy session for database operations
    
    Yields:
        Database session
    """
    yield from get_database_session()


# Re-export current member dependency
def get_current_member(
    member: Member = Depends(get_authenticated_member)
) -> Member:
    """
    Get current authenticated member
    Use this dependency in protected routes
    
    Args:
        member: Authenticated member from auth service
        
    Returns:
        Current member object
    """
    return member


def require_admin(
    current_member: Member = Depends(get_current_member)
) -> Member:
    """
    Require admin privileges
    Use this dependency for admin-only routes
    
    Args:
        current_member: Current authenticated member
        
    Returns:
        Current member if admin
        
    Raises:
        HTTPException: If member is not admin
    """
    # Check if member has admin privileges
    # For now, we'll check if membership_tier is 'admin'
    # You can customize this logic based on your admin identification method
    
    if not hasattr(current_member, 'membership_tier'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Administrative privileges required."
        )
    
    # Check various admin identifiers
    is_admin = (
        current_member.membership_tier == "admin" or
        current_member.email.endswith("@paigeinnercircle.com") or  # Staff emails
        getattr(current_member, 'is_admin', False)  # If you add is_admin field
    )
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This area is reserved for administrators only."
        )
    
    return current_member


def verify_member_active(
    current_member: Member = Depends(get_current_member)
) -> Member:
    """
    Verify member account is active
    Additional check beyond authentication
    
    Args:
        current_member: Current authenticated member
        
    Returns:
        Current member if active
        
    Raises:
        HTTPException: If member is not active
    """
    if not current_member.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently inactive. Please contact support for assistance."
        )
    
    return current_member


# Optional: Pagination dependency
class PaginationParams:
    """
    Pagination parameters for list endpoints
    """
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100
    ):
        self.skip = skip
        self.limit = min(limit, 100)  # Cap at 100 items per page


def get_pagination(
    skip: int = 0,
    limit: int = 100
) -> PaginationParams:
    """
    Pagination dependency
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        
    Returns:
        PaginationParams object
    """
    return PaginationParams(skip=skip, limit=limit)