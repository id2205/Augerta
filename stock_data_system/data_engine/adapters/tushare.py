import pandas as pd
import tushare as ts
from ..models.stock import StockInfo

from typing import List

import logging

class TushareAdapter:
    def __init__(self, config):
        self.config = config
        ts.set_token(self.config.TUSHARE_TOKEN)
        self.pro = ts.pro_api()

    def get_daily_data(self, symbol: str) -> pd.DataFrame:
        df = self.pro.daily(ts_code=symbol, adj='qfq', freq='D')
        # 检查 df 是否为 None
        if df is None:
            logging.warning(f"Failed to fetch daily data for symbol: {symbol}")
            return pd.DataFrame()  # 返回空的 DataFrame
        return self._format_data(df)

    def get_minute_data(self, symbol):
        try:
            # 假设这里是获取数据的代码
            df = self._fetch_minute_data(symbol)
            if df is None:
                logging.error(f"Failed to fetch minute data for symbol {symbol}")
                return None
            return self._format_minute_data(df)
        except Exception as e:
            logging.error(f"Error fetching minute data for symbol {symbol}: {e}")
            return None

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # 数据字段转换逻辑
        return df.rename(columns={
            'ts_code': 'symbol',
            'trade_date': 'date',
            'vol': 'volume',
            'amount': 'turnover'
        })

    def _format_minute_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['datetime'] = pd.to_datetime(df['trade_time'])
        return df.rename(columns={
            'ts_code': 'symbol',
            'trade_time': 'timestamp',
            'vol': 'volume',
            'amount': 'turnover'
        })

    def _fetch_minute_data(self, symbol):
        try:
            # 直接调用Tushare API获取分钟数据
            result = self.pro.bar(ts_code=symbol, freq='1min')
            return result
        except Exception as e:
            logging.error(f"获取{symbol}分钟数据失败: {e}")
            return None
        
        # 删除重复的类定义
        import tushare as ts
        
        class TushareAdapter:
            def __init__(self, config):
                self.config = config
                self.pro = ts.pro_api(self.config.TUSHARE_TOKEN)
        
            def get_minute_data(self, symbol):
                try:
                    # 确保正确调用 Tushare API
                    result = self.pro.bar(ts_code=symbol, freq='1min')
                    return result
                except Exception as e:
                    logging.error(f"Error fetching minute data for symbol {symbol}: {e}")
                    return None

    def get_stock_list(self):
        """
        获取沪深A股的所有股票清单
        :return: 包含股票清单的 DataFrame，如果失败则返回空的 DataFrame
        """
        try:
            # 使用 Tushare 的 stock_basic 接口获取沪深A股的股票清单
            df = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            if df is None:
                logging.warning("Failed to fetch stock list.")
                return pd.DataFrame()
            return df
        except Exception as e:
            logging.error(f"Error fetching stock list: {e}")
            return pd.DataFrame()