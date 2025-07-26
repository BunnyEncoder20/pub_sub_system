from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"

    name = Column(String(100), nullable=False, index=True)
    device_type = Column(String(50), nullable=False)
    status = Column(String(20), default="active")
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    locations = relationship("Location", back_populates="device", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', type='{self.device_type}')>"