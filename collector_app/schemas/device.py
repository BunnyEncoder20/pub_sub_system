from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy.sql.sqltypes import UUID


class DeviceCreate(BaseModel):
    device_id: str = Field(...,example='device_123')
    name: str = Field(..., exmaple='Temperature Sensor')
    type: Optional[str] = Field(None, example='Sensor')
    status: Optional[str] = Field(None, exmaple='active')

class DeviceResponse(BaseModel):
    id: UUID
    device_id: str
    name: str
    type: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True
