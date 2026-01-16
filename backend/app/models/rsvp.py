from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class RSVP(Base):
    __tablename__ = "rsvps"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    
    # RSVP Details
    status = Column(String, nullable=False)  # "accepted", "declined", "pending"
    response_message = Column(Text, nullable=True)  # Optional personal note
    
    # Timestamps
    responded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="rsvps")
    event = relationship("Event", back_populates="rsvps")
    
    def __repr__(self):
        return f"<RSVP {self.status} by Member {self.member_id}>"