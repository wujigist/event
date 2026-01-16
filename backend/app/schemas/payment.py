from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class PaymentBase(BaseModel):
    """Base payment schema"""
    amount: Decimal = Decimal("1000.00")
    currency: str = "USD"


class PaymentMethodResponse(BaseModel):
    """Available payment methods"""
    methods: list[dict[str, str]]


class PaymentContactSubmit(BaseModel):
    """Schema for submitting payment contact info"""
    legacy_token: UUID
    contact_email: EmailStr
    payment_method: str


class PaymentContactResponse(BaseModel):
    """Response after contact submission"""
    message: str
    status: str
    next_steps: str
    estimated_contact_time: str


class PaymentResponse(PaymentBase):
    """Payment response"""
    id: UUID
    member_id: UUID
    legacy_pass_id: UUID
    payment_method: Optional[str]
    contact_email: str
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PaymentStatusResponse(BaseModel):
    """Payment verification status"""
    payment_id: UUID
    status: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    can_access_full_pass: bool
    message: str


class PaymentVerify(BaseModel):
    """Schema for admin to verify payment"""
    payment_id: UUID
    verified_by: str
    notes: Optional[str] = None


class PaymentVerifiedResponse(BaseModel):
    """Response after payment verification"""
    message: str
    payment: PaymentResponse
    full_pass_access_granted: bool