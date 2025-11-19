from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cooperativista_id = Column(Integer, ForeignKey("cooperativistas.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # IDENTIFICACIÓN DEL DISPOSITIVO
    device_id = Column(String(255), unique=True, nullable=False, index=True)
    device_name = Column(String(100))
    device_model = Column(String(100))
    device_os = Column(String(50))
    
    # SEGURIDAD
    api_key_hash = Column(String(255), nullable=False)
    auth_method = Column(String(20))
    
    # ESTADO
    is_active = Column(Boolean, default=True, index=True)
    is_blocked = Column(Boolean, default=False)
    block_reason = Column(Text)
    
    # AUDITORÍA
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    registered_by = Column(Integer, ForeignKey("users.id"))
    last_seen = Column(DateTime(timezone=True))
    last_activity = Column(DateTime(timezone=True))
    revoked_at = Column(DateTime(timezone=True))
    revoked_by = Column(Integer, ForeignKey("users.id"))
    
    # RELACIONES
    cooperativista = relationship("Cooperativista", back_populates="devices")