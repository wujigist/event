from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class RSVPBase(BaseModel):
    """Base RSVP schema"""
    status: str  # "accepted" or "declined"
    response_message: Optional[str] = None


class RSVPCreate(RSVPBase):
    """Schema for creating RSVP"""
    event_id: UUID


class RSVPUpdate(BaseModel):
    """Schema for updating RSVP"""
    status: Optional[str] = None
    response_message: Optional[str] = None


class RSVPResponse(RSVPBase):
    """Schema for RSVP response"""
    id: UUID
    member_id: UUID
    event_id: UUID
    responded_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RSVPAcceptedResponse(BaseModel):
    """Response when RSVP is accepted"""
    message: str
    rsvp: RSVPResponse
    legacy_token: UUID
    next_steps: str


class RSVPDeclinedResponse(BaseModel):
    """Response when RSVP is declined"""
    message: str
    rsvp: RSVPResponse
    appreciation_message: str


class RSVPStatusResponse(BaseModel):
    """Current RSVP status"""
    has_rsvp: bool
    status: Optional[str] = None
    rsvp: Optional[RSVPResponse] = None