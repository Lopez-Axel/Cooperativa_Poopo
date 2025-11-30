# models/device.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cooperativista_id = Column(Integer, ForeignKey("cooperativistas.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # IDENTIFICACIÓN DEL DISPOSITIVO
    device_id = Column(String(255), unique=True, nullable=True, index=True)  # Ahora nullable hasta que se active
    device_name = Column(String(100))
    device_model = Column(String(100))
    device_os = Column(String(50))
    
    # SEGURIDAD
    api_key_hash = Column(String(255), nullable=False)
    api_key_plain = Column(String(64), unique=True, nullable=False, index=True)  # NUEVO: Para validación
    auth_method = Column(String(20), default="api_key")
    
    # ESTADO
    is_active = Column(Boolean, default=False, index=True)  # False hasta que se active desde app
    is_activated = Column(Boolean, default=False, index=True)  # NUEVO: Indica si ya vinculó dispositivo
    is_blocked = Column(Boolean, default=False)
    block_reason = Column(Text)
    
    # AUDITORÍA
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    registered_by = Column(Integer, ForeignKey("users.id"))
    activated_at = Column(DateTime(timezone=True))  # NUEVO: Cuando vinculó el dispositivo
    last_seen = Column(DateTime(timezone=True))
    last_activity = Column(DateTime(timezone=True))
    revoked_at = Column(DateTime(timezone=True))
    revoked_by = Column(Integer, ForeignKey("users.id"))
    
    # RELACIONES
    cooperativista = relationship("Cooperativista", back_populates="devices")