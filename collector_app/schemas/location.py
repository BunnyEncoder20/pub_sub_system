from decimal import FloatOperation
from typing import Optional
from pydnactic import BaseModel, Field
from datetime import datetime

class LocationCreate(BaseModel):
    device_id: str = Field(..., exmaple='device_123')
    latitude: float = Field(..., exmaple=12.9716)
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
