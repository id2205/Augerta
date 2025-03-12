from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, PrimaryKeyConstraint, UniqueConstraint,Boolean

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stocks'
    from sqlalchemy import Sequence
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String, unique=True)
    symbol = Column(String)
    name = Column(String)
    area = Column(String)
    industry = Column(String)
    # 其他字段...


class MinuteQuote(Base):
    __tablename__ = 'minute_quotes'
    from sqlalchemy import Sequence
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String)
    trade_time = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    vol = Column(Float)
    amount = Column(Float)
    __table_args__ = (UniqueConstraint('ts_code', 'trade_time'),)    

class DailyData(Base):
    __tablename__ = 'daily_data'
    from sqlalchemy import Sequence
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String)
    trade_date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    pre_close = Column(Float)
    change = Column(Float)
    pct_chg = Column(Float)
    vol = Column(Float)
    amount = Column(Float)
    __table_args__ = (UniqueConstraint('ts_code', 'trade_date'),)    


class Index(Base):
    __tablename__ = 'indexes'
    from sqlalchemy import Sequence
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String)
    trade_date = Column(String)
    close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    pre_close = Column(Float)
    change = Column(Float)
    pct_chg = Column(Float)
    vol = Column(Float)
    amount = Column(Float)

class Industry(Base):
    __tablename__ = 'industries'
    from sqlalchemy import Sequence
    id = Column(Integer, primary_key=True, autoincrement=True)
    index_code = Column(String)
    index_name = Column(String)
    market = Column(String)


class CallAuctionData(Base):
    __tablename__ = 'call_auction_data'
    from sqlalchemy import Sequence
    id = Column(Integer, Sequence('table_id_seq'), primary_key=True)
    ts_code = Column(String)
    trade_date = Column(String)
    vol = Column(Integer)
    price = Column(Integer)
    amount = Column(Float)
    pre_close = Column(Float)
    turnover_rate = Column(Float)
    volume_ratio = Column(Float)
    float_share = Column(Float)
    __table_args__ = (UniqueConstraint('ts_code', 'trade_date'),)


#id = Column(Integer, Sequence('table_id_seq'), primary_key=True)


class ThsIndex(Base):
    __tablename__ = 'ths_indexes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String, unique=True)
    name = Column(String)
    count = Column(Integer)
    exchange = Column(String)
    list_date = Column(Date)
    type = Column(String)

class ThsMember(Base):
    __tablename__ = 'ths_members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String)
    con_code = Column(String)
    con_name = Column(String)
    weight = Column(Float)
    in_date = Column(Date)
    out_date = Column(Date)
    is_new = Column(Boolean)
    __table_args__ = (UniqueConstraint('ts_code', 'con_code'),)
