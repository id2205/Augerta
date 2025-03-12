from apscheduler.schedulers.background import BackgroundScheduler
from Augerta.data_engine.data_fetcher import fetch_and_save_stock_data,fetch_and_save_call_auction_data
import datetime

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    start_date = datetime.date.today().strftime('%Y%m%d')
    end_date = datetime.date.today().strftime('%Y%m%d')
    start_time = '09:30:00'
    end_time = '15:00:00'
    # 每个交易日早上9点执行股票信息数据定时任务
    #scheduler.add_job(lambda: get_base_data(get_pro_api()), 'cron', day_of_week='mon-fri', hour=9)
    # 每个交易日下午15:01执行股票及日线行情数据定时任务
    scheduler.add_job(lambda: fetch_and_save_stock_data(start_date,end_date), 'cron', day_of_week='mon-fri',hour=15, minute=1)
    #竞价结果数据每天9:25:02执行
    scheduler.add_job(lambda: fetch_and_save_call_auction_data(start_date,end_date), 'cron', day_of_week='mon-fri',hour=9, minute=25,second=2)
    scheduler.start()
    
    try:
        # 保持程序运行
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()