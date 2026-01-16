from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Payment(Base):
    __tablename__ = "payments"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    legacy_pass_id = Column(UUID(as_uuid=True), ForeignKey("legacy_passes.id"), nullable=False)
    
    # Payment Details
    amount = Column(Numeric(10, 2), default=1000.00, nullable=False)
    currency = Column(String, default="USD")
    payment_method = Column(String, nullable=True)  # Selected payment method
    contact_email = Column(String, nullable=False)  # Email for payment contact
    
    # Status
    status = Column(String, default="pending")  # pending, verified, failed
    
    # Verification
    verified_by = Column(String, nullable=True)  # Admin who verified
    verified_at = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)  # Admin notes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="payments")
    legacy_pass = relationship("LegacyPass", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment ${self.amount} - {self.status}>"