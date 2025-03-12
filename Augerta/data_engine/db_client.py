from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date, Sequence, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models.stock import Stock, DailyData,Index,Industry,CallAuctionData,ThsIndex,ThsMember

# 创建会话类
Session = sessionmaker()

Base = declarative_base()

engine = create_engine('sqlite:///stock_data.db')
Session.configure(bind=engine)


def save_base_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            stock = session.query(Stock).filter_by(ts_code=row['ts_code']).first()
            if stock:
                # 更新现有记录
                for key, value in row.items():
                    setattr(stock, key, value if key in row else None)
            else:
                # 插入新记录
                stock = Stock(
                    ts_code=row['ts_code'],
                    symbol = row['symbol'] if 'symbol' in row else None,
                    name=row['name'] if 'name' in row else None,
                    area=row['area'] if 'area' in row else None,
                    industry=row['industry'] if 'industry' in row else None,
                )
            session.add(stock)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_index_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            index_data = Index(
                ts_code=row['ts_code'],
                trade_date=row['trade_date'],
                close=row['close'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                pre_close=row['pre_close'],
                change=row['change'],
                pct_chg=row['pct_chg'],
                vol=row['vol'],
                amount=row['amount']
            )
            session.add(index_data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_industry_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            industry = Industry(
                index_code=row['index_code'],
                index_name=row['index_name'],
                market=row['market']
            )
            session.add(industry)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_daily_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            daily_data = session.query(DailyData).filter_by(ts_code=row['ts_code'], trade_date=row['trade_date']).first()
            if daily_data:
                # 更新现有记录
                for key, value in row.items():
                    setattr(daily_data, key, value if key in row else None)
            else:
                # 插入新记录
                daily_data = DailyData(
                    ts_code=row['ts_code'],
                    trade_date=row['trade_date'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    pre_close=row['pre_close'],
                    change=row['change'],
                    pct_chg=row['pct_chg'],
                    vol=row['vol'],
                    amount=row['amount']
                )
            session.add(daily_data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_minute_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            existing_record = session.query(MinuteQuote).filter_by(ts_code=row['ts_code'], trade_time=row['trade_time']).first()
            if existing_record:
                # 如果存在，更新记录
                for key, value in row.items():
                    setattr(existing_record, key, value if key in row else None)
            else:
                # 如果不存在，插入新记录
                new_record = MinuteQuote(
                    ts_code=row['ts_code'],
                    trade_time=row['trade_time'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    vol=row['vol'],
                    amount=row['amount']
                )
                session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"保存分钟数据时出错: {e}")
    finally:
        session.close()


class DatabaseClient:
    def __init__(self, config):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        self.engine = create_engine(config.DATABASE_URI)
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False)

    def initialize(self):
        from ..models.base import Base
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def execute_query(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            result = conn.execute(query, params or {})
            return result.fetchall()
    def bulk_insert(self, model, records):
        session = self.SessionLocal()
        try:
            session.bulk_insert_mappings(model, records)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# 保存同花顺概念指数数据
import pandas as pd
def save_ths_index(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        # 直接处理单条数据
        ths_index = session.query(ThsIndex).filter_by(ts_code=data['ts_code']).first()
        if ths_index:
            # 更新现有记录
            for key, value in data.items():
                setattr(ths_index, key, value if key in data else None)
        else:
            # 插入新记录
            ths_index = ThsIndex(
                ts_code=data['ts_code'],
                name=data['name'] if 'name' in data else None,
                count=data['count'] if 'count' in data else None,
                exchange=data['exchange'] if 'exchange' in data else None,
                list_date=data['list_date'] if 'list_date' in data else None,
                type=data['type'] if 'type' in data else None
            )
        session.add(ths_index)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# 保存同花顺概念板块成分数据
def save_ths_member(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            ths_member = session.query(ThsMember).filter_by(ts_code=row['ts_code'], con_code=row['con_code']).first()
            if ths_member:
                # 更新现有记录
                for key, value in row.items():
                    setattr(ths_member, key, value if key in row else None)
            else:
                # 插入新记录
                ths_member = ThsMember(
                    ts_code=row['ts_code'],
                    con_code=row['con_code'] if 'con_code' in row else None,
                    con_name=row['con_name'] if 'con_name' in row else None,
                    weight=row['weight'] if 'weight' in row else None,
                    in_date=row['in_date'] if 'in_date' in row else None,
                    out_date=row['out_date'] if 'out_date' in row else None,
                    is_new=row['is_new'] if 'is_new' in row else None
                )
            session.add(ths_member)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_call_auction_data(data):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for index, row in data.iterrows():
            call_auction_data = session.query(CallAuctionData).filter_by(ts_code=row['ts_code'], trade_date=row['trade_date']).first()
            if call_auction_data:
                # 更新现有记录
                for key, value in row.items():
                    setattr(call_auction_data, key, value if key in row else None)
            else:
                # 插入新记录
                call_auction_data = CallAuctionData(
                    ts_code=row['ts_code'],
                    trade_date=row['trade_date'],
                    vol=row['vol'],
                    price=row['price'],
                    amount=row['amount'],
                    pre_close=row['pre_close'],
                    turnover_rate=row['turnover_rate'],
                    volume_ratio=row['volume_ratio'],
                    float_share=row['float_share']
                )
            session.add(call_auction_data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    def save_market_data(data):
    # 由于未定义Market模型，这里暂时不做处理
        pass

def get_call_auction_data_by_date(date):
    Base.metadata.create_all(engine)
    session = Session()
    try:
        data = session.query(CallAuctionData, Stock.name).join(Stock, CallAuctionData.ts_code == Stock.ts_code).filter(CallAuctionData.trade_date == date).all()
        result = []
        for call_auction, stock_name in data:
            call_auction_dict = call_auction.__dict__
            call_auction_dict['stock_name'] = stock_name
            print(stock_name)
            result.append(call_auction_dict)
        return result
    except Exception as e:
        print(f"查询集合竞价数据时出错: {e}")
        return []
    finally:
        session.close()

def get_stocks_from_table():
    Base.metadata.create_all(engine)
    session = Session()
    try:
        data = session.query(Stock).all()
        result = []
        for stock in data:
            stock_dict = stock.__dict__
            stock_dict.pop('_sa_instance_state', None)
            result.append(stock_dict)
        return result
    except Exception as e:
        print(f"查询股票数据时出错: {e}")
        return []
    finally:
        session.close()
