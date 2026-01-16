from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Event(Base):
    __tablename__ = "events"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Event Information
    title = Column(String, nullable=False)  # e.g., "Paige's Inner Circle Evening"
    subtitle = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    
    # Date & Time
    event_date = Column(DateTime, nullable=False)
    event_time = Column(String, nullable=False)  # e.g., "7:00 PM EST"
    
    # Venue
    venue_name = Column(String, nullable=False)
    venue_address = Column(Text, nullable=False)
    
    # Event Details
    dress_code = Column(String, nullable=True)  # e.g., "Black Tie"
    theme = Column(String, nullable=True)
    
    # Complex Data (stored as JSON)
    schedule = Column(JSON, nullable=True)  # Timeline of event
    amenities = Column(JSON, nullable=True)  # List of luxury amenities
    special_instructions = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")
    legacy_passes = relationship("LegacyPass", back_populates="event", cascade="all, delete-orphan")
    memories = relationship("Memory", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event {self.title}>"