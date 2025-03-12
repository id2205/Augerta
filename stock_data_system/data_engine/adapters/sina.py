import pandas as pd
import requests
from datetime import datetime
from ..models.stock import Stock

class SinaAdapter:
    def __init__(self, config):
        self.base_url = 'http://hq.sinajs.cn/list='
    
    def get_minute_data(self, symbol: str) -> pd.DataFrame:
        response = requests.get(f"{self.base_url}{symbol}")
        response.encoding = 'gbk'
        data = response.text.split('="')[1].split(',')
        
        return pd.DataFrame({
            'symbol': [symbol],
            'timestamp': [datetime.now()],
            'open': [float(data[1])],
            'high': [float(data[4])],
            'low': [float(data[5])],
            'close': [float(data[3])],
            'volume': [int(data[8])],
            'bid1': [float(data[11])],
            'bid1_volume': [int(data[12])],
            'bid2': [float(data[13])],
            'bid2_volume': [int(data[14])],
            'bid3': [float(data[15])],
            'bid3_volume': [int(data[16])],
            'bid4': [float(data[17])],
            'bid4_volume': [int(data[18])],
            'bid5': [float(data[19])],
            'bid5_volume': [int(data[20])],
            'ask1': [float(data[21])],
            'ask1_volume': [int(data[22])],
            'ask2': [float(data[23])],
            'ask2_volume': [int(data[24])],
            'ask3': [float(data[25])],
            'ask3_volume': [int(data[26])],
            'ask4': [float(data[27])],
            'ask4_volume': [int(data[28])],
            'ask5': [float(data[29])],
            'ask5_volume': [int(data[30])]
        })