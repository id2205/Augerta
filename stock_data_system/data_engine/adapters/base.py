from abc import ABC, abstractmethod
import pandas as pd

class DataAdapter(ABC):
    @abstractmethod
    def get_daily_data(self, symbol: str) -> pd.DataFrame:
        """获取日级别行情数据"""
        
    @abstractmethod 
    def get_minute_data(self, symbol: str) -> pd.DataFrame:
        """获取分钟级别行情数据"""

class AdapterFactory:
    @staticmethod
    def create_adapter(config) -> DataAdapter:
        if config.DATA_SOURCE == 'tushare':
            return TushareAdapter(config)
        elif config.DATA_SOURCE == 'mairui':
            return MairuiAdapter(config)
        raise ValueError("Unsupported data source")