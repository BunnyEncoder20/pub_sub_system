from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from shared.database.session import get_db
from schemas.device import DeviceSchema

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix="/v1/api/device",
    tags=["Posts"]
)

'''------------------------------ APIs ------------------------------'''

@router.post('/create')
def create_device(device: DeviceSchema, db: Session = Depends(get_db)):
    ''' Adds a new device to the DB '''
    pass

@ router.get('/')
def get_devices(device_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''  Returns one or all devices '''
    pass

@router.delete('/{device_id}')
def delete_device(device_id: str, db: Session = Depends(get_db)):
    ''' Deletes a device by ID '''
    pass
