import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from stock_data_system.config.settings import Config
import logging
from stock_data_system.data_engine.models.stock import StockInfo, DailyData, MinuteData
from stock_data_system.service.scheduler import DataScheduler

# 初始化配置
config = Config()
config.init_app(None)  # 传入None作为app参数

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        scheduler = DataScheduler()
        scheduler.start()
        logging.info('DataScheduler started successfully')
        while True:
            pass
    except Exception as e:
        logging.error(f'Failed to start scheduler: {e}')