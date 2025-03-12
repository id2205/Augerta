from Augerta.data_engine.db_client import get_call_auction_data_by_date
import pandas as pd

import threading

# 为每个线程创建独立的数据库会话
thread_local = threading.local()

def get_call_auction_data(date):
    # 获取当前线程的数据库会话
    if not hasattr(thread_local, 'session'):
        from Augerta.data_engine.db_client import Session
        thread_local.session = Session()
    data = get_call_auction_data_by_date(date, session=thread_local.session)
    df = pd.DataFrame(data)
    if len(df) == 0:
        return None
    df = df.drop(columns=['_sa_instance_state'])
    return df