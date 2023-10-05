from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class Priority(Base):
    __tablename__ = 'priority'

    priority_id = Column(Integer, primary_key=True)
    publication_id = Column(Integer)
    category_id = Column(Integer)
    priority = Column(Integer)

