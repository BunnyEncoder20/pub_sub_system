from fastapi import APIRouter, Depends, status, HTTPException

from typing import Optional, List
from sqlalchemy.orm import Session
from shared.database.session import get_db
from shared.rabbitmq.publisher import RabbitMQPublisher, get_rabbitmq_producer
from shared.models.location import Location
from collector_app.schemas.location import LocationCreate, LocationResponse
from logger import get_logger
from app_config import settings

'''------------------------------------------------------------------'''

router = APIRouter(
    prefix=settings.app.API_V1_PREFIX+"/location",
    tags=["Location"]
)

logger = get_logger(__name__)

'''------------------------------ APIs ------------------------------'''

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def create_location(location: LocationCreate, producer: RabbitMQPublisher = Depends(get_rabbitmq_producer)):
    """ Publishes location data to RabbitMQ """
    logger.info('create_location_requested')
    logger.debug('payload_received', data=location.model_dump())

    try:
        location_data = location.model_dump_json()
        producer.publish_to_exchange(
            exchange_name=settings.rabbitmq.EXCHANGE_NAME,
            routing_key=settings.rabbitmq.ROUTING_KEY,
            message=location_data
        )
        logger.info('location_published_to_rabbitmq', status='success')
        return {"status": "Location data published successfully"}

    except Exception as e:
        logger.error(
            'location_publishing_failed',
            status='failure',
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to publish location data.")

@router.get('/last_locations', response_model=List[LocationResponse])
def get_last_locations(device_id: Optional[str] = None, db: Session = Depends(get_db)):
    """ Fetches last known location(s) """
    logger.info('get_last_locations_requested', device_id=device_id)

    try:
        if device_id:
            last_location = db.query(Location).filter(Location.device_id == device_id).order_by(Location.timestamp.desc()).first()
            if not last_location:
                logger.warn('last_location_not_found', device_id=device_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Last location not found for this device.")
            logger.info('last_location_found', device_id=device_id, location_id=last_location.id)
            return [last_location]

        # If no device_id is provided, get the last location for all devices
        subquery = db.query(Location.device_id, func.max(Location.timestamp).label('max_timestamp')).group_by(Location.device_id).subquery()
        last_locations = db.query(Location).join(
            subquery,
            (Location.device_id == subquery.c.device_id) & (Location.timestamp == subquery.c.max_timestamp)
        ).all()

        logger.info('last_locations_found_for_all_devices', count=len(last_locations))
        return last_locations

    except Exception as e:
        logger.error(
            'get_last_locations_failed',
            status='failure',
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to fetch last locations.")

@router.get('/history', response_model=List[LocationResponse])
def get_location_history(device_id: str, db: Session = Depends(get_db)):
    """  Fetches full location history for a specific device """
    logger.info('get_location_history_requested', device_id=device_id)

    try:
        location_history = db.query(Location).filter(Location.device_id == device_id).order_by(Location.timestamp.desc()).all()

        if not location_history:
            logger.warn('location_history_not_found', device_id=device_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location history not found for this device.")

        logger.info('location_history_found', device_id=device_id, count=len(location_history))
        return location_history

    except Exception as e:
        logger.error(
            'get_location_history_failed',
            status='failure',
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to fetch location history.")
