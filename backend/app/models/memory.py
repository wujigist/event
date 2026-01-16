from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Memory(Base):
    __tablename__ = "memories"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    
    # Memory Assets
    photo_gallery_url = Column(String, nullable=True)
    thank_you_video_url = Column(String, nullable=True)
    certificate_pdf_path = Column(String, nullable=True)
    
    # Collectible Badge
    badge_number = Column(Integer, nullable=True)  # e.g., #001
    badge_image_path = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="memories")
    event = relationship("Event", back_populates="memories")
    
    def __repr__(self):
        return f"<Memory for Member {self.member_id}>"