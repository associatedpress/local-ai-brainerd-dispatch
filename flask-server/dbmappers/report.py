from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create a declarative base object
Base = declarative_base()

# define the Report class
class Report(Base):
    __tablename__ = 'report'

    report_id = Column(Integer, primary_key=True)
    report_dt = Column(DateTime)
    report_created_by_userid = Column(Integer)
    publication_id = Column(Integer)
    case_id = Column(Integer)
    report_sent_to_vender = Column(Boolean)
    report_sent_dt = Column(DateTime)
    report_sent_by_userid = Column(Integer)