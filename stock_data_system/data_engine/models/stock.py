from sqlalchemy import Column, String, Date, Boolean, PrimaryKeyConstraint
from .base import Base

class StockInfo(Base):
    __tablename__ = 'stock_info'

    symbol = Column(String(12), primary_key=True)
    name = Column(String(64))
    exchange = Column(String(16))
    industry = Column(String(32))
    list_date = Column(String(8))
    status = Column(String(8), default='L')

    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, name={self.name})>"


class DailyData(Base):
    __tablename__ = 'daily_data'

    date = Column(Date, primary_key=True)
    symbol = Column(String(12), primary_key=True)
    open = Column(String(16))
    high = Column(String(16))
    low = Column(String(16))
    close = Column(String(16))
    volume = Column(String(32))

    def __repr__(self):
        return f"<Daily(symbol={self.symbol}, date={self.date})>"


class MinuteData(Base):
    __tablename__ = 'minute_data'

    datetime = Column(Date, primary_key=True)
    symbol = Column(String(12), primary_key=True)
    open = Column(String(16))
    high = Column(String(16))
    low = Column(String(16))
    close = Column(String(16))
    volume = Column(String(32))

    def __repr__(self):
        return f"<Minute(symbol={self.symbol}, datetime={self.datetime})>"