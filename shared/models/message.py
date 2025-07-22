# shared/models/message.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from shared.models.base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), default="received")  # or published/processed

    def __repr__(self):
        return f"<Message(id={self.id}, device_id={self.device_id}, status='{self.status}')>"
