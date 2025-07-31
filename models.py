from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from db import Base

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    premium_amount = Column(String)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
