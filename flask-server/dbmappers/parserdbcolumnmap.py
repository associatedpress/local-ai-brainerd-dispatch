from sqlalchemy import create_engine, Column, Text, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a declarative base object
Base = declarative_base()

# define the User class
class ParserColumnMap(Base):
    __tablename__ = 'parse_col_map'

    pcm_id = Column(Integer, primary_key=True)
    parser_id = Column(Integer)
    agency_id = Column(Integer)
    parser_colname = Column(String(256))
    db_colname = Column(String(256))
    

