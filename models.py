from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"
    claim_id = Column(String, primary_key=True)
    provider_id = Column(String, ForeignKey("providers.provider_id"))
    risk_id = Column(String, ForeignKey("risks.risk_id"))
    summary = Column(String)
    status = Column(String, default="Pending")  # Pending/Approved/Denied
    reason_code = Column(String, nullable=True)
    reason_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Provider(Base):
    __tablename__ = "providers"
    provider_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    location = Column(String)

class Risk(Base):
    __tablename__ = "risks"
    risk_id = Column(String, primary_key=True)
    risk_level = Column(String)  # low/medium/high
    risk_description = Column(String)