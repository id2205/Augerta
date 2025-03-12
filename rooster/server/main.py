# coding=utf-8
from __future__ import print_function, absolute_import
from datetime import datetime, timedelta
from gm.api import set_token, history
from rooster.integration.myquantServices import MyQuantService
from rooster.services.stock_data import (
    init_db,
    init_api,
    get_stock_symbols,
    update_stock_info,
    fetch_daily_data,
    fetch_all_daily_data,
    get_stock_info
)
import pandas as pd


# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式
# 设置token， 查看已有token ID,在用户-密钥管理里获取
set_token('cb3ca858dfd6aec54ce4e4a8b9eac460d806baeb')

# 获取所有沪深A股
myquant_service = MyQuantService(api_key='your_api_key_here')
stocks = myquant_service.get_symbols(exchange='SHSE,SZSE')

# 获取最近30天的涨停板数据
limit_up_data = []
for i in range(30):
    date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    try:
        daily_data = myquant_service.get_historical_data(
            symbol=stocks['symbol'].tolist(),
            start_date=date + ' 09:00:00',
            end_date=date + ' 16:00:00'
        )
        print(f"Data for {date}:")
        if len(daily_data) > 0:
            print(daily_data.head())  # Print first few rows
            limit_up_count = len(daily_data)
        else:
            print("No data returned")
            limit_up_count = 0
    except Exception as e:
        print(f"Error fetching data for {date}: {str(e)}")
        limit_up_count = 0
    limit_up_data.append({'date': date, 'limit_up_count': limit_up_count})

# 转换为DataFrame
data = pd.DataFrame(limit_up_data)
print(data)
