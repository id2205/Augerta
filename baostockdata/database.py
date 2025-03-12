import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    
    # 创建stock_basic_info表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_basic_info (
            stock_code TEXT PRIMARY KEY,
            stock_name TEXT,
            list_date TEXT,
            industry TEXT,
            pe REAL,
            pb REAL,
            total_market_cap REAL,
            circulate_market_cap REAL
        )
    ''')
    
    # 创建stock_trade_data表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_trade_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT,
            trade_date TEXT,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            volume INTEGER,
            turnover REAL
        )
    ''')
    
    conn.commit()

def insert_basic_info(conn, data):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO stock_basic_info 
        (stock_code, stock_name, list_date, industry, pe, pb, total_market_cap, circulate_market_cap)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

def fetch_basic_info(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM stock_basic_info
    ''')
    return cursor.fetchall()

def fetch_trade_data(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM stock_trade_data
    ''')
    return cursor.fetchall()

def insert_trade_data(conn, data):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stock_trade_data 
        (stock_code, trade_date, open_price, high_price, low_price, close_price, volume, turnover)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

def connect_db():
    return sqlite3.connect('stock_data.db')
