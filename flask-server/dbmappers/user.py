from sqlalchemy import create_engine, Column, Text, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(256))
    user_password = Column(Text)
    user_firstname = Column(String(256))
    user_lastname = Column(String(256))
    #pubid = Column(String(256))

