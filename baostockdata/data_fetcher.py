import baostock as bs
import pandas as pd
from datetime import datetime, timedelta

def get_stock_basic_info(stock_code):
    rs = bs.query_stock_basic_info(stock_code)
    data_list = []
    while rs.next():
        data = rs.get_row_data()
        data_list.append(data)
    return data_list

def query_history_k_data_plus(stock_code, start_date, end_date, frequency='5'):
    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,open,high,low,close,volume,turnover",
                                      start_date=start_date,
                                      end_date=end_date,
                                      frequency=frequency,
                                      adjustflag='2')
    data_list = []
    while rs.next():
        data = rs.get_row_data()
        data_list.append(data)
    return data_list

def fetch_all_stocks():
    rs = bs.query_stock_basic_info()
    stock_list = []
    while rs.next():
        stock = rs.get_row_data()
        stock_list.append((stock[0], stock[1]))
    return stock_list
