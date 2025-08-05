from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.config import settings

engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    Base.metadata.create_all(bind=engine)
    return SessionLocal()
