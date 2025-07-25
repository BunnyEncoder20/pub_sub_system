from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.sql.sqltypes import UUID



class DeviceCreate(BaseModel):
    name: str = Field(..., exmaple='Temperature Sensor')
    type: Optional[str] = Field(None, example='Sensor')
    status: Optional[str] = Field(None, exmaple='active')
    description: Optional[str] = Field(None, example='reports temp very 60s')
    is_active: bool = Field(True, example='True')

class DeviceResponse(BaseModel):
    id: UUID
    name: str
    type: Optional[str]
    status: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
