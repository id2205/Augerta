import tushare as ts
import os
from dotenv import load_dotenv
import pandas as pd
from Augerta.data_engine.adapters.tushare import TushareAdapter

# 一次性获取A股股票base全量数据
def fetch_stock_basic_data():
    return TushareAdapter.get_stock_basic_data()

# 获取单个股股票某一时间段的日线行情数据
def fetch_stock_daily_data(ts_code, start_date, end_date):
    return TushareAdapter.get_stock_daily_data(ts_code, start_date, end_date)

# 获取同花顺概念指数数据
def fetch_ths_index():
    return TushareAdapter.get_ths_index()

# 获取同花顺概念板块成分数据
def fetch_ths_member(ts_code):
    return TushareAdapter.get_ths_member(ts_code)

#获取当日个股和ETF的集合竞价成交情况，每天9点25后可以获取当日的集合竞价成交数据
#每分钟可以调用10次，限量：单次最大返回8000行数据，可根据日期或代码循环获取全部历史
def fetch_stk_auction(index_code,trade_date, start_date, end_date):
    return pro.stk_auction(ts_code=index_code,trade_date = trade_date, start_date=start_date, end_date=end_date)


# 获取指数实时信息数据的逻辑
def get_industry_data():
    return pro.index_basic(market='SW')

# 获取index数据
def fetch_index_data(index_code, start_date, end_date):
    return pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)



