from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    device_id = Column(String(255), unique=True, nullable=False, index=True)
    device_name = Column(String(100))
    device_model = Column(String(100))
    device_os = Column(String(50))
    
    is_active = Column(Boolean, default=True, index=True)
    
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    deactivated_at = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="devices")
