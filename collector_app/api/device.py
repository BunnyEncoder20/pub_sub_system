from starlette.status import HTTP_404_NOT_FOUND
from collector_app.schemas import device
from logger import get_logger
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from shared.database.session import get_db
from shared.models.device import Device
from schemas.device import DeviceCreate, DeviceResponse
from app_config import settings

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix=settings.app.API_V1_PREFIX+"device",
    tags=["Device"]
)

logger = get_logger(__name__)

'''------------------------------ APIs ------------------------------'''

@router.post('/create', response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    ''' Adds a new device to the DB '''
    logger.info('create_device_requested')
    logger.debug('payload_received', data=device.model_dump())

    try:
        new_device = Device(
            name = device.name,
            device_type = device.type,
            status = device.status,
            description = device.description,
            is_active = device.is_active
        )
        logger.info(f"Device ORM object created")

        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        logger.info('device_created', status='success', device_added=new_device)

        return new_device

    except Exception as e:
           logger.error(
               'device_creation_failed',
               status='failure',
               error=str(e)
           )
           raise HTTPException(status_code=500, detail="Device creation failed.")

@router.get('/', response_model=List[DeviceResponse])
def get_devices(device_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''  Returns one or all devices '''

    if device_id:
        logger.info('get_device_requested', device_id=device_id)

        found_device = db.query(Device).filter(Device.id == device_id).first()

        if not found_device:
            logger.exception('device_not_found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Device not found')

        logger.info('device_found', device_id=found_device.id)
        return list(found_device)


    logger.info('get_device_requested', device_id=None)
    devices = db.query(Device).all()
    return devices



@router.delete('/{device_id}')
def delete_device(device_id: str, db: Session = Depends(get_db)):
    ''' Deletes a device by ID '''

    logger.info('delete_device_requested', device_id=device_id)

    found_device = db.query(Device).filter(Device.id == device_id).first()

    if not found_device:
        logger.error('device_not_found', device_id=device_id)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Device not found')

    db.delete(device)
    db.commit()

    logger.info('device_deleted', device_id=device_id)
    return {
        'status': status.HTTP_200_OK,
        'message':f'Device [{device_id}] deleted successfully',
    }
