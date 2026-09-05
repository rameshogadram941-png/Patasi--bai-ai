from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsageEvent(Base):
    __tablename__ = 'usage_events'
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String(128), index=True, nullable=False)
    endpoint = Column(String(64), nullable=False)
    request_tokens = Column(Integer, default=0)
    response_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
