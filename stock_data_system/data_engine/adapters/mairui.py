import pandas as pd
import requests
from datetime import datetime
from typing import List
from ..models.stock import Stock
from ..models.trade import MinuteKline

class MairuiAdapter:
    def __init__(self, config):
        self.api_key = config.MAIRUI_API_KEY
        self.secret = config.MAIRUI_SECRET
        self.base_url = 'https://api.mairui.club/v1'

    def _make_request(self, endpoint, params):
        headers = {
            'X-API-KEY': self.api_key,
            'X-API-SECRET': self.secret
        }
        response = requests.get(f"{self.base_url}/{endpoint}", params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_daily_data(self, symbol: str) -> pd.DataFrame:
        data = self._make_request('daily', {'symbol': symbol})
        df = pd.DataFrame(data['items'])
        return self._format_daily_data(df)

    def get_minute_data(self, symbol: str) -> pd.DataFrame:
        data = self._make_request('minute', {'symbol': symbol})
        df = pd.DataFrame(data['items'])
        return self._format_minute_data(df)

    def _format_daily_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['date'] = pd.to_datetime(df['trade_date'])
        return df.rename(columns={
            'ts_code': 'symbol',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'vol': 'volume',
            'amount': 'turnover'
        })[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'turnover']]

    def _format_minute_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['timestamp'] = pd.to_datetime(df['trade_time'])
        return df.rename(columns={
            'ts_code': 'symbol',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'vol': 'volume',
            'amount': 'turnover'
        })[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']]