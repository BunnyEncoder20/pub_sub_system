from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str

class Device(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class LocationCreate(BaseModel):
    device_id: int
    latitude: float
    longitude: float

class Location(BaseModel):
    id: int
    device_id: int
    latitude: float
    longitude: float
    timestamp: datetime

    class Config:
        orm_mode = True