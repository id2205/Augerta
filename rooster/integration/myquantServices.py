from typing import List, Dict, Any
import pandas as pd
import logging
from gm.api import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MyQuantService:
    def __init__(self, api_key: str):
        """初始化MyQuant服务
        
        Args:
            api_key: MyQuant API key
        """
        set_token(api_key)

    def get_symbols(self, exchange: str = None, product_type: str = None) -> pd.DataFrame:
        """获取标的列表
        
        Args:
            exchange: 交易所代码
            product_type: 产品类型
            
        Returns:
            pd.DataFrame: 包含标的信息的DataFrame
        """
        try:
            # 调用gm.api的get_symbol_infos方法
            symbols = get_symbol_infos(sec_type1=1010, exchanges='SHSE,SZSE')
            
            # 转换为DataFrame并映射字段
            df = pd.DataFrame(symbols)
            df = df.rename(columns={
                'code': 'symbol',
                'name': 'name',
                'exchange': 'exchange',
                'sector': 'industry',
                'list_date': 'list_date'
            })
            logger.info(f"Successfully fetched {len(df)} symbols")
            
            # 只保留需要的字段
            return df[['symbol', 'name', 'exchange', 'industry', 'list_date']]
            
        except Exception as e:
            logger.error(f"Error fetching symbols: {str(e)}")
            raise
