import schedule
import time
from data_fetcher import fetch_all_stocks, get_stock_basic_info, query_history_k_data_plus
from database import connect_db, insert_basic_info, insert_trade_data

def update_stock_basic_info():
    conn = connect_db()
    stocks = fetch_all_stocks()
    for stock_code, stock_name in stocks:
        basic_info = get_stock_basic_info(stock_code)
        for info in basic_info:
            insert_basic_info(conn, info)
    conn.close()

def update_stock_trade_data():
    conn = connect_db()
    stocks = fetch_all_stocks()
    today = datetime.today().strftime('%Y-%m-%d')
    start_date = '2025-01-01'
    for stock_code, _ in stocks:
        data = query_history_k_data_plus(stock_code, start_date, today)
        for item in data:
            insert_trade_data(conn, item)
    conn.close()

schedule.every(1).day.at("09:00").do(update_stock_basic_info)  # 每天9点更新基本信息
schedule.every(1).day.at("16:00").do(update_stock_trade_data)  # 每天16点更新交易数据

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
