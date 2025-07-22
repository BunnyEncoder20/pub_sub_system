from sqlalchemy import Column, String, Boolean, Text
from shared.models.base import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"

    name = Column(String(100), nullable=False, index=True)
    device_type = Column(String(50), nullable=False)
    status = Column(String(20), default="active")
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', type='{self.device_type}')>"
