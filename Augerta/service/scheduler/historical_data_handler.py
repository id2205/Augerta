import tushare as ts
from Augerta.data_engine.db_client import save_base_data, save_index_data,save_daily_data,save_minute_data,save_call_auction_data,save_ths_index,save_ths_member
from Augerta.data_engine.adapters.data_fetch import get_base_data,get_stk_auction
from Augerta.config.settings import TUSHARE_TOKEN
import pandas as pd

# 初始化Tushare
pro = ts.pro_api(TUSHARE_TOKEN)

# 获取股票历史数据
# 修改为使用stock_basic接口
def get_stock_historical_data(ts_code, start_date, end_date):
    try:
        #data = pro.stock_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        print(f'data = ', data)
        return data
    except Exception as e:
        print(f'获取股票历史数据失败: {e}')
        return None

# 函数为获取股票日线行情
def get_stock_daily_historical_data(ts_code, start_date, end_date):
    try:
        data = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if data is not None:
            data['trade_date'] = pd.to_datetime(data['trade_date'])
        return data
    except Exception as e:
        print(f'获取行情日线历史数据失败: {e}')
        return None

# 获取行情历史数据
# 修改为使用stk_mins接口获取分钟行情，使用daily接口获取日线行情


# 获取指数历史数据
def get_index_historical_data(index_code, start_date, end_date):
    try:
        data = pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)
        if data is not None:
            data['trade_date'] = pd.to_datetime(data['trade_date'])
        return data
    except Exception as e:
        print(f'获取指数历史数据失败: {e}')
        return None


# 拉取并保存历史数据

# 获取集合竞价历史数据
# 新增拉取并保存集合竞价历史数据的逻辑
# 新增一个函数用于获取集合竞价历史数据
def get_stock_call_auction_data(trade_date, start_date, end_date):
    try:
        data = get_stk_auction(pro, '', trade_date, start_date, end_date)
        return data
    except Exception as e:
        print(f'获取集合竞价历史数据失败: {e}')
        return None

# 拉取并保存集合竞价历史数据
# 新增拉取并保存集合竞价历史数据的逻辑
def fetch_and_save_call_auction_data(start_date, end_date):
    start_date_str = pd.to_datetime(start_date).strftime('%Y%m%d')
    end_date_str = pd.to_datetime(end_date).strftime('%Y%m%d')
    current_date = pd.to_datetime(start_date)
    while current_date <= pd.to_datetime(end_date):
        trade_date = current_date.strftime('%Y%m%d')
        
        call_auction_data = get_stock_call_auction_data(trade_date, start_date_str, end_date_str)
        print('trade_date = ', trade_date,'call_auction_data =',call_auction_data)
        if call_auction_data is not None:
            save_call_auction_data(call_auction_data)
        current_date = current_date + pd.Timedelta(days=1)

# 拉取并保存历史数据
# 新增拉取并保存行情分钟历史数据的逻辑
def fetch_and_save_historical_data(stock_codes, index_codes, start_date, end_date, start_time, end_time):
    # 拉取并保存股票历史数据
    stock_data = get_stock_historical_data(stock_codes, start_date, end_date)
    save_base_data(stock_data)
    stock_codes = stock_data.ts_code

    # 拉取并保存行情日线历史数据
    for stock_code in stock_codes:
        print('stock_code = ', stock_code)
        daily_data = get_stock_daily_historical_data(stock_code, start_date, end_date)
        if daily_data is not None:
            save_daily_data(daily_data)
        # 拉取并保存行情分钟历史数据
        #stock_minute_data = get_stock_minute_data(stock_code, start_time, end_time)
        #if stock_minute_data is not None:
        #    save_minute_data(stock_minute_data)

    # 拉取并保存指数历史数据
    #for index_code in index_codes:
        # index_data = get_index_historical_data(index_code, start_date, end_date)
        # if index_data is not None:
        #     save_index_data(index_data)

    # 拉取并保存行情分钟历史数据
    #for stock_code in stock_codes:
        #market_minute_data = get_market_minute_data(stock_code, start_time, end_time)
        # if market_minute_data is not None:
        #     save_market_data(market_minute_data)



# 获取同花顺概念指数数据
# 新增拉取并保存同花顺概念指数及成分股数据的逻辑
# 新增一个函数用于获取同花顺概念指数数据
import logging

def get_ths_index_data(pro):
    try:
        # 查询A股所有概念指数
        ths_index = pro.ths_index(type='N')
        return ths_index
    except Exception as e:
        logging.error(f'获取同花顺概念指数数据失败: {e}')
        return None

# 获取同花顺概念板块成分数据
# 新增一个函数用于获取同花顺概念板块成分数据
# 每个概念指数后查询对应的成分股
# 分别落库
# 分别保存到数据库
def get_ths_member_data(pro, ts_code):
    try:
        # 查询成分股
        ths_member = pro.ths_member(ts_code=ts_code)
        return ths_member
    except Exception as e:
        logging.error(f'获取同花顺概念板块成分数据失败: {e}')
        return None

# 拉取并保存同花顺概念指数及成分股数据
# 新增拉取并保存同花顺概念指数及成分股数据的逻辑
def fetch_and_save_ths_index_and_member_data():
    # 删除原有的日期处理逻辑
    ths_index = get_ths_index_data(pro)
    print('ths_index = ', ths_index)
    if ths_index is not None:
        for index, row in ths_index.iterrows():
            ts_code = row['ts_code']  
            print('ts_code = ', ts_code)                      
            # 将日期字符串转换为日期对象
            row['list_date'] = datetime.datetime.strptime(row['list_date'], '%Y%m%d').date()
            save_ths_index(row)
            ths_member = get_ths_member_data(pro, ts_code)
            if ths_member is not None:
                list_date = pd.to_datetime(row['list_date']).date()
            # 将日期字符串转为日期对象
            row['list_date'] = list_date
if __name__ == '__main__':
    stock_codes = ['000001.SZ', '000002.SZ']  # 示例股票代码
    index_codes = ['000001.SH']  # 示例指数代码
    start_date = '20250101'
    end_date = datetime.date.today().strftime('%Y%m%d')
    start_time = '09:30:00'
    end_time = '15:00:00'
    fetch_and_save_call_auction_data(start_date, end_date)
    # 修改调用处，去掉参数
    #fetch_and_save_ths_index_and_member_data()
    #fetch_and_save_historical_data(stock_codes, index_codes, start_date, end_date, start_time, end_time)