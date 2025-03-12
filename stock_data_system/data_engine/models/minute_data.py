from sqlalchemy import Column, String, DateTime, Float, PrimaryKeyConstraint
from stock_data_system.data_engine.models.base import Base

class MinuteData(Base):
    __tablename__ = 'minute_data'
    __table_args__ = (
        PrimaryKeyConstraint('ts_code', 'trade_time'),
    )

    ts_code = Column(String(20))
    trade_time = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    vol = Column(Float)
    amount = Column(Float)