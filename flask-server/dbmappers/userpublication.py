from sqlalchemy import create_engine, Column, Text, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class UserPublication(Base):
    __tablename__ = 'user_pub'

    user_pub_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    publication_id = Column(Integer)
    

