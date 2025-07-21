from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class DeviceType(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    CONTROLLER = "controller"
    GATEWAY = "gateway"


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Device name")
    device_type: DeviceType = Field(..., description="Type of device")
    status: DeviceStatus = Field(default=DeviceStatus.ACTIVE, description="Device status")
    description: Optional[str] = Field(None, max_length=1000, description="Device description")
    is_active: bool = Field(default=True, description="Whether device is active")


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    device_type: Optional[DeviceType] = None
    status: Optional[DeviceStatus] = None
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DeviceMessage(BaseModel):
    """Message schema for RabbitMQ communication"""
    device_id: int
    action: str = Field(..., description="Action performed (create, update, delete)")
    data: dict = Field(..., description="Device data")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
