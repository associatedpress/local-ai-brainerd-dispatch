from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class State(Base):
    __tablename__ = 'state'

    state_id = Column(Integer, primary_key=True)
    state_name = Column(String(256))
    usps_state_abbrrevation = Column(String(256))

