from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from typing import Optional
from shared.database.session import get_db

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix="/v1/api/location",
    tags=["Posts"]
)

'''------------------------------ APIs ------------------------------'''

@router.post('/')
def create_location(location: LocationSchema, producer: RabbitMQPublisher = Depends(get_rabbitmq_producer)):
    ''' Publishes location data to RabbitMQ '''
    pass

@ router.get('/last_locations')
def get_last_locations(device_id: Optional[str] = None, db: Session = Depends(get_db)):
    ''' Fetches last known location(s) '''
    pass

@router.get('/history')
def get_location_history(device_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''  Fetches full location history '''
    pass
