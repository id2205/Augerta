import logging  # 新增日志模块导入

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_data_system.data_engine.db_client import DatabaseClient
from stock_data_system.data_engine.models import StockInfo, DailyData, MinuteData
from stock_data_system.data_engine.adapters.tushare import TushareAdapter
from datetime import datetime, time
import pandas as pd
from config.settings import Config  # 新增配置类导入

class DataScheduler:
    def __init__(self):
        self.config = Config()
        self.config.init_app(None)
        logging.info('Initializing DataScheduler with config: %s', self.config)
        self.scheduler = BackgroundScheduler()
        # 移除重复的DevelopmentConfig导入和赋值
        self.db_client = DatabaseClient(self.config)
        self.adapter = TushareAdapter(self.config)
        
        # 新增数据库初始化
        self.db_client.initialize()
        
        # 添加定时任务
        self.scheduler.add_job(
            self.update_stock_list,
            CronTrigger(day_of_week='mon-fri', hour=13, minute=49)
        )
        self.scheduler.add_job(
            self.update_daily_data,
            CronTrigger(day_of_week='mon-fri', hour=15, minute=1)
        )
        self.scheduler.add_job(
            self.update_minute_data,
            CronTrigger(day_of_week='mon-fri', hour='9-11,13-14,15', minute='30-59/1', second=0)
        )

    def is_trading_day(self):
        '''交易日判断逻辑'''
        today = datetime.now().strftime('%Y%m%d')
        # 调用Tushare交易日历接口
        df = self.adapter.pro.trade_cal(exchange='', start_date=today, end_date=today)
        if not df.empty and df.iloc[0]['is_open'] == 1:
            return True
        return False

    def update_stock_list(self):
        if self.is_trading_day():
            data = self.adapter.get_stock_list()
            self.db_client.bulk_insert(StockInfo, data.to_dict('records'))

    def update_daily_data(self):
        if self.is_trading_day():
            symbols = [s.ts_code for s in self.db_client.get_session().query(StockInfo)]
            for symbol in symbols:
                df = self.adapter.get_daily_data(symbol)
                self.db_client.bulk_insert(DailyData, df.to_dict('records'))

    def update_minute_data(self):
        current_time = datetime.now().time()
        logging.info(f"开始执行分钟数据更新任务，当前时间：{current_time}")
        
        if self.is_trading_day() and \
           ((time(9,30) <= current_time <= time(11,30)) or \
            (time(13,0) <= current_time <= time(15,0))):
            
            symbols = [s.ts_code for s in self.db_client.get_session().query(StockInfo)]
            logging.info(f"待处理股票数量：{len(symbols)}，示例股票代码：{symbols[:3]}")
            
            for symbol in symbols:
                try:
                    logging.info(f"开始获取 {symbol} 分钟数据")
                    raw_df = self.adapter.get_minute_data(symbol)
                    
                    if raw_df is None:
                        logging.warning(f"{symbol} 未获取到原始数据")
                        continue
                        
                    logging.info(f"{symbol} 原始数据获取成功，条数：{len(raw_df)}，字段：{list(raw_df.columns)}")
                    logging.debug(f"样本原始数据：\n{raw_df.head(1).to_dict()}")
                    
                    df = self._format_minute_data(raw_df)
                    logging.info(f"数据转换完成，转换后字段：{list(df.columns)}")
                    logging.debug(f"样本转换后数据：\n{df.head(1).to_dict()}")
                    
                    if not df.empty:
                        record_count = len(df.to_dict('records'))
                        self.db_client.bulk_insert(MinuteData, df.to_dict('records'))
                        logging.info(f"成功插入 {record_count} 条分钟数据")
                    else:
                        logging.warning(f"{symbol} 转换后数据为空，跳过插入")
                        
                except Exception as e:
                    logging.error(f"更新 {symbol} 分钟数据失败", exc_info=True)
                    logging.error(f"错误详情：{str(e)}")
                    
            logging.info("分钟数据更新任务执行完毕")
        else:
            logging.warning(f"当前时间 {current_time} 不在交易时段内，跳过执行")

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()