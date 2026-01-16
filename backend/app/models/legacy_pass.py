from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class LegacyPass(Base):
    __tablename__ = "legacy_passes"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    
    # Pass Details
    pass_number = Column(String, unique=True, nullable=False)  # e.g., "INNER-CIRCLE-#001"
    unique_token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    
    # Tier & Access
    access_level = Column(String, default="gold")  # gold, platinum, diamond
    gift_tier = Column(String, default="standard")  # standard, premium, elite
    seating_category = Column(String, nullable=True)  # VIP, Premium, etc.
    
    # QR Code & Assets
    qr_code_data = Column(Text, nullable=True)
    qr_code_image_path = Column(String, nullable=True)
    
    # Pass Images
    pass_front_image_path = Column(String, nullable=True)
    pass_back_image_path = Column(String, nullable=True)
    full_pass_pdf_path = Column(String, nullable=True)
    blurred_preview_path = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="legacy_passes")
    event = relationship("Event", back_populates="legacy_passes")
    payment = relationship("Payment", back_populates="legacy_pass", uselist=False)
    
    def __repr__(self):
        return f"<LegacyPass {self.pass_number}>"