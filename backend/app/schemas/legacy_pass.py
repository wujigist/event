from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class LegacyPassBase(BaseModel):
    """Base legacy pass schema"""
    access_level: str = "gold"
    gift_tier: str = "standard"
    seating_category: Optional[str] = None


class LegacyPassCreate(LegacyPassBase):
    """Schema for creating legacy pass"""
    member_id: UUID
    event_id: UUID
    pass_number: str


class LegacyPassResponse(LegacyPassBase):
    """Basic legacy pass response"""
    id: UUID
    member_id: UUID
    event_id: UUID
    pass_number: str
    unique_token: UUID
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LegacyPassPreview(BaseModel):
    """Blurred preview of legacy pass"""
    pass_number_partial: str  # e.g., "INNER-CIRCLE-#***"
    event_name: str
    event_date: str
    benefits_preview: list[str]
    payment_required: bool
    payment_amount: float
    blurred_image_url: Optional[str] = None


class LegacyPassFull(LegacyPassResponse):
    """Complete legacy pass details (after payment)"""
    qr_code_data: Optional[str]
    qr_code_image_url: Optional[str]
    pass_front_image_url: Optional[str]
    pass_back_image_url: Optional[str]
    full_pass_pdf_url: Optional[str]
    gift_list: list[str]
    amenities_list: list[str]
    seating_info: Optional[str]
    special_perks: list[str]


class LegacyPassDownload(BaseModel):
    """Download URLs for legacy pass"""
    pdf_url: str
    front_image_url: str
    back_image_url: str
    apple_wallet_url: Optional[str] = None
    google_wallet_url: Optional[str] = None


class LegacyPassBenefits(BaseModel):
    """Benefits unlocked by legacy pass"""
    access_level: str
    gift_tier: str
    gifts: list[str]
    amenities: list[str]
    seating_category: Optional[str]
    special_perks: list[str]