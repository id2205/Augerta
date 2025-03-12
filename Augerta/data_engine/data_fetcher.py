# 导入必要的库
import tushare as ts
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from .adapters.data_fetch import fetch_stock_basic_data,fetch_stock_daily_data,fetch_stk_auction
from .db_client import save_base_data,save_daily_data,save_call_auction_data

# 拉取并保存股票基本信息以及日线行情数据
def fetch_and_save_stock_data( start_date, end_date):
    # 拉取并保存股票历史数据
    stock_data = fetch_stock_basic_data()
    save_base_data(stock_data)
    stock_codes = stock_data.ts_code

    # 拉取并保存行情日线历史数据
    for stock_code in stock_codes:
        print('stock_code = ', stock_code)
        daily_data = fetch_stock_daily_data(stock_code, start_date, end_date)
        if daily_data is not None:
            save_daily_data(daily_data)

# 拉取并保存集合竞价历史数据
# 新增拉取并保存集合竞价历史数据的逻辑
def fetch_and_save_call_auction_data(start_date, end_date):
    start_date_str = pd.to_datetime(start_date).strftime('%Y%m%d')
    end_date_str = pd.to_datetime(end_date).strftime('%Y%m%d')
    current_date = pd.to_datetime(start_date)
    while current_date <= pd.to_datetime(end_date):
        trade_date = current_date.strftime('%Y%m%d')
        
        call_auction_data = fetch_stk_auction(trade_date, start_date_str, end_date_str)
        print('trade_date = ', trade_date,'call_auction_data =',call_auction_data)
        if call_auction_data is not None:
            save_call_auction_data(call_auction_data)
        current_date = current_date + pd.Timedelta(days=1)