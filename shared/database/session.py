from logging import getLogger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from shared.config import shared_settings

logger = getLogger(__name__)

try:
    engine = create_engine(shared_settings.database.database_url)
    logger.info("SQLAlchemy engine created successfully")
except Exception as e:
   logger.error(f"Failed to create SQLAlchemy engine: {e}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    '''
    Dependency that yields a database session
    '''
    db = SessionLocal()
    logger.debug("Database session opened")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")
