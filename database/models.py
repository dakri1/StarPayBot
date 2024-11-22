from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, index=True)
    paid = Column(Boolean)
    subscription_end_date = Column(DateTime)
