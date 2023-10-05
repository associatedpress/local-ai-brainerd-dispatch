from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeneralSetting(Base):
    __tablename__ = 'general_settings'

    gs_id = Column(Integer, primary_key=True)
    gs_name = Column(String(256))
    gs_value = Column(Text)
