from datetime import datetime
import os
import pandas as pd
import sqlite3
from gm.api import set_token, history, get_symbol_infos
from sqlalchemy import create_engine
import logging
from .config import CONFIG

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('stock_data.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Initialize database
DB_ENGINE = create_engine(CONFIG['database_uri'])

def initialize_database():
    """Initialize database tables"""
    try:
        with DB_ENGINE.connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stock_info (
                    symbol TEXT PRIMARY KEY,
                    name TEXT,
                    exchange TEXT,
                    industry TEXT,
                    list_date DATE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS daily_data (
                    date DATE,
                    symbol TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    PRIMARY KEY (date, symbol)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS minute_data (
                    timestamp DATETIME,
                    symbol TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    PRIMARY KEY (timestamp, symbol)
                )
            ''')
            logger.info("Database tables initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False

def fetch_stock_symbols():
    """Fetch all stock symbols using Quantaxis API"""
    try:
        symbols = get_symbol_infos()
        symbols = pd.DataFrame(symbols)
        symbols = symbols[['symbol', 'name', 'exchange']]
        return symbols
    except Exception as e:
        logger.error(f"Failed to fetch stock symbols: {str(e)}")
        return pd.DataFrame()

def fetch_daily_data(symbol, date):
    """Fetch daily data for a single stock"""
    try:
        data = history(
            symbol=symbol,
            start_time=f"{date} 09:30:00",
            end_time=f"{date} 15:00:00",
            frequency='1d',
            fields='symbol,open,high,low,close,volume',
            df=True
        )
        if not data.empty:
            return data
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to fetch daily data for {symbol}: {str(e)}")
        return pd.DataFrame()

def fetch_minute_data(symbol, date):
    """Fetch minute data for a single stock"""
    try:
        data = history(
            symbol=symbol,
            start_time=f"{date} 09:30:00",
            end_time=f"{date} 15:00:00",
            frequency='1min',
            fields='symbol,open,high,low,close,volume',
            df=True
        )
        if not data.empty:
            return data
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to fetch minute data for {symbol}: {str(e)}")
        return pd.DataFrame()

def update_stock_info():
    """Update stock information"""
    try:
        symbols = fetch_stock_symbols()
        if not symbols.empty:
            with DB_ENGINE.connect() as conn:
                symbols.to_sql('stock_info', conn, if_exists='replace', index=False)
                logger.info("Stock information updated successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to update stock info: {str(e)}")
        return False

def update_daily_data(date=None):
    """Update daily data for all stocks"""
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        symbols = pd.read_sql_query("SELECT symbol FROM stock_info", DB_ENGINE)
        data = []
        
        for symbol in symbols['symbol'].tolist():
            daily_data = fetch_daily_data(symbol, date)
            if not daily_data.empty:
                data.append(daily_data)
        
        if data:
            df = pd.concat(data, ignore_index=True)
            with DB_ENGINE.connect() as conn:
                df.to_sql('daily_data', conn, if_exists='append', index=False)
                logger.info(f"Daily data updated for {len(data)} symbols")
        return True
    except Exception as e:
        logger.error(f"Failed to update daily data: {str(e)}")
        return False

def update_minute_data(date=None):
    """Update minute data for all stocks"""
    try:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        symbols = pd.read_sql_query("SELECT symbol FROM stock_info", DB_ENGINE)
        data = []
        
        for symbol in symbols['symbol'].tolist():
            minute_data = fetch_minute_data(symbol, date)
            if not minute_data.empty:
                data.append(minute_data)
        
        if data:
            df = pd.concat(data, ignore_index=True)
            with DB_ENGINE.connect() as conn:
                df.to_sql('minute_data', conn, if_exists='append', index=False)
                logger.info(f"Minute data updated for {len(data)} symbols")
        return True
    except Exception as e:
        logger.error(f"Failed to update minute data: {str(e)}")
        return False

def create_web_interface():
    """Create a simple web interface to query and display stock info"""
    try:
        from flask import Flask, render_template
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return render_template('index.html')
            
        @app.route('/query', methods=['GET'])
        def query():
            symbol = request.args.get('symbol', '')
            if not symbol:
                return "Please provide a symbol"
                
            df = pd.read_sql_query(f"SELECT * FROM stock_info WHERE symbol = '{symbol}'", DB_ENGINE)
            return df.to_html()
            
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Failed to create web interface: {str(e)}")

if __name__ == '__main__':
    initialize_database()
    update_stock_info()
    update_daily_data()
    update_minute_data()
    create_web_interface()
