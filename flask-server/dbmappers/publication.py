from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class Publication(Base):
    __tablename__ = 'publication'

    publication_id = Column(Integer, primary_key=True) 
    publication_name = Column(String(256))
    city = Column(String(256))
    state_id = Column(Integer)
    vendor_id = Column(String(256))

