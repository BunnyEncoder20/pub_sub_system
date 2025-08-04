from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataItem(Base):
    __tablename__ = "data_items"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
