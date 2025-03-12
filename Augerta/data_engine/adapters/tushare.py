import tushare as ts
import pandas as pd
from Augerta.config.settings import TUSHARE_TOKEN


class TushareAdapter:
    #def __init__(self, token):
    #    self.pro = ts.pro_api(token)
    #load_dotenv()
    #token = os.getenv('TUSHARE_TOKEN')
    pro = ts.pro_api(TUSHARE_TOKEN)
    # 初始化pro接口
    def get_pro_api():
        return ts.pro_api(token)

    # 获取base数据
    def get_stock_basic_data():
        # 实现获取base数据的逻辑
        return TushareAdapter.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    # 函数为获取股票日线行情
    def get_stock_daily_data(ts_code, start_date, end_date):
        try:
            data = TushareAdapter.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if data is not None:
                data['trade_date'] = pd.to_datetime(data['trade_date'])
            return data
        except Exception as e:
            print(f'获取行情日线历史数据失败: {e}')
            return None

    # 新增一个函数用于获取分钟行情，暂时没有权限，只能调用两次
    def get_stock_minute_data(ts_code, start_time, end_time):
        try:
            data = TushareAdapter.pro.stk_mins(ts_code=ts_code,freq = 1, start_time=start_time, end_time=end_time)
            return data
        except Exception as e:
            print(f'获取行情分钟历史数据失败: {e}')
            return None

    # 实现获取industry数据的逻辑
    def get_industry_data():
        return TushareAdapter.pro.index_basic(market='SW')

    # 获取指数日线数据
    def get_index_data(index_code, start_date, end_date):
        return TushareAdapter.pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)

    # 获取同花顺概念指数数据
    def get_ths_index():
        return TushareAdapter.pro.ths_index(type='N')

    # 根据同花顺概念板块代码获取成分股数据
    def get_ths_member(ts_code):
        return TushareAdapter.pro.ths_member(ts_code=ts_code)

    #获取当日个股和ETF的集合竞价成交情况，每天9点25后可以获取当日的集合竞价成交数据
    #每分钟可以调用10次，限量：单次最大返回8000行数据，可根据日期或代码循环获取全部历史
    def get_stk_auction(index_code,trade_date, start_date, end_date):
        return TushareAdapter.pro.stk_auction(ts_code=index_code,trade_date = trade_date, start_date=start_date, end_date=end_date)
    
    # 新增一个函数用于获取集合竞价历史数据
    def get_stock_call_auction_data(trade_date, start_date, end_date):
        try:
            data = get_stk_auction(TushareAdapter.pro, '', trade_date, start_date, end_date)
            return data
        except Exception as e:
            print(f'获取集合竞价历史数据失败: {e}')
            return None