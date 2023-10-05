from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class Agency(Base):
    __tablename__ = 'agency'

    agency_id = Column(Integer, primary_key=True)
    agency_name = Column(String(256))
    parser_id = Column(Integer)
    city = Column(String(256))
    state_id = Column(Integer)

