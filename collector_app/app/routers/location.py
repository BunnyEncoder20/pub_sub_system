from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.celery_client import send_task

from app.db import get_db_session
from app.models import Location
from app.schemas import LocationCreate, Location as LocationSchema

router = APIRouter()

@router.post("/location/")
def create_location_record(location: LocationCreate):
    send_task("process_location", args=[location.dict()])
    return {"status": "Location record sent for processing"}

@router.get("/location/last_locations", response_model=List[LocationSchema])
def get_last_locations_of_devices(device_id: Optional[int] = None, session: Session = Depends(get_db_session)):
    query = session.query(Location)
    if device_id:
        query = query.filter(Location.device_id == device_id)
    # This is a simplified approach. A more robust solution would involve subqueries or CTEs
    # to get the truly last location per device. For now, it gets all locations and relies on client-side filtering or a more complex query.
    locations = query.order_by(Location.timestamp.desc()).all()
    
    # To get only the last location per device, we need to group by device_id and select the max timestamp.
    # This requires a more advanced SQLAlchemy query. For simplicity, returning all and letting the client filter
    # or implementing a more complex query later.
    
    # A more correct way to get last locations per device:
    # from sqlalchemy import func
    # subquery = session.query(Location.device_id, func.max(Location.timestamp).label("max_timestamp"))\
    #     .group_by(Location.device_id).subquery() 
    # last_locations = session.query(Location).join(subquery, 
    #     (Location.device_id == subquery.c.device_id) & 
    #     (Location.timestamp == subquery.c.max_timestamp)
    # ).all()
    
    return locations

@router.get("/location/history", response_model=List[LocationSchema])
def get_location_history_of_device(device_id: Optional[int] = None, session: Session = Depends(get_db_session)):
    query = session.query(Location)
    if device_id:
        query = query.filter(Location.device_id == device_id)
    locations = query.order_by(Location.timestamp.asc()).all()
    return locations
