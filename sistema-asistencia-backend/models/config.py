from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base

class Config(Base):
    __tablename__ = "config"

    key = Column(String(50), primary_key=True)
    value = Column(Text)
    description = Column(Text)
    data_type = Column(String(20))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"))