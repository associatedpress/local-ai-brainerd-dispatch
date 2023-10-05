from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CaseDetail(Base):
    __tablename__ = 'casedetail'

    case_id = Column(Integer, primary_key=True)
    case_number = Column(String(256))
    case_desc = Column(Text)
    category_id = Column(Integer)
    reported_dt = Column(DateTime)
    names_involved = Column(Text)
    officers_involved = Column(Text)
    agency_id = Column(Integer)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    address_line1 = Column(Text)
    city = Column(String(256))
    zipcode = Column(String(256))
    state_id = Column(Integer)
    upload_userid = Column(Integer)
    upload_dt = Column(DateTime)
    resoource_id = Column(String(1000))
    is_ignored = Column(Boolean)
