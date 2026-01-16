from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID


class EventBase(BaseModel):
    """Base event schema"""
    title: str
    subtitle: Optional[str] = None
    description: str
    event_date: datetime
    event_time: str
    venue_name: str
    venue_address: str
    dress_code: Optional[str] = None
    theme: Optional[str] = None


class EventCreate(EventBase):
    """Schema for creating an event (Admin only)"""
    schedule: Optional[Dict[str, Any]] = None
    amenities: Optional[Dict[str, Any]] = None
    special_instructions: Optional[str] = None


class EventUpdate(BaseModel):
    """Schema for updating event"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_time: Optional[str] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    dress_code: Optional[str] = None
    theme: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    amenities: Optional[Dict[str, Any]] = None
    special_instructions: Optional[str] = None
    is_active: Optional[bool] = None


class EventResponse(EventBase):
    """Basic event response"""
    id: UUID
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EventDetail(EventResponse):
    """Detailed event response with all luxury details"""
    schedule: Optional[Dict[str, Any]] = None
    amenities: Optional[Dict[str, Any]] = None
    special_instructions: Optional[str] = None


class EventTeaser(BaseModel):
    """Limited event info for public landing page"""
    id: UUID  # ← ADD THIS
    title: str
    subtitle: Optional[str]
    event_date: datetime
    theme: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)