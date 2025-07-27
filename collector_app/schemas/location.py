from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class LocationCreate(BaseModel):
    device_id: str = Field(..., example='device_123')
    latitude: float = Field(..., example=12.9716)
    longitude: float = Field(..., example=77.5946)
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class LocationResponse(BaseModel):
    id: int
    device_id: str
    latitude: float
    longitude: float
    timestamp: datetime

    class Config:
        orm_mode = True