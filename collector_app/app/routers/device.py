from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db_session
from app.models import Device
from app.schemas import DeviceCreate, Device as DeviceSchema

router = APIRouter()

@router.post("/device/create", response_model=DeviceSchema)
def create_device(device: DeviceCreate, session: Session = Depends(get_db_session)):
    db_device = Device(name=device.name)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.get("/device", response_model=List[DeviceSchema])
def get_device(device_id: Optional[int] = None, session: Session = Depends(get_db_session)):
    if device_id:
        device = session.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return [device]
    devices = session.query(Device).all()
    return devices

@router.delete("/device/delete/{device_id}")
def delete_device(device_id: int, session: Session = Depends(get_db_session)):
    device = session.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    return {"message": "Device deleted successfully"}
