from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Member(Base):
    __tablename__ = "members"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Personal Information
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    
    # Membership Details
    membership_tier = Column(String, default="inner_circle")  # founding_member, inner_circle
    membership_number = Column(String, unique=True, nullable=True)  # e.g., "IC-001"
    
    # Status
    is_active = Column(Boolean, default=True)
    has_logged_in = Column(Boolean, default=False)
    
    # Session Management
    access_token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rsvps = relationship("RSVP", back_populates="member", cascade="all, delete-orphan")
    legacy_passes = relationship("LegacyPass", back_populates="member", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="member", cascade="all, delete-orphan")
    memories = relationship("Memory", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member {self.full_name} ({self.email})>"