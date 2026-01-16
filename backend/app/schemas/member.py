from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class MemberBase(BaseModel):
    """Base member schema with common fields"""
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None


class MemberCreate(MemberBase):
    """Schema for creating a new member (Admin only)"""
    membership_tier: Optional[str] = "inner_circle"
    membership_number: Optional[str] = None


class MemberLogin(BaseModel):
    """Schema for member login/access request"""
    email: EmailStr


class MemberResponse(MemberBase):
    """Schema for member response"""
    id: UUID
    membership_tier: str
    membership_number: Optional[str]
    is_active: bool
    has_logged_in: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MemberDashboard(MemberResponse):
    """Extended member info for dashboard"""
    # Can add additional computed fields here
    pass


class MemberUpdate(BaseModel):
    """Schema for updating member details"""
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    membership_tier: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    member: MemberResponse