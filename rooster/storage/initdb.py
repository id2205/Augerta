from sqlalchemy import create_engine
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

def init_db():
    """Initialize database with stock_info and stock_daily tables"""
    try:
        engine = create_engine('sqlite:///rooster/stock_data.db')
        
        with engine.connect() as conn:
            # Drop existing tables if they exist
            conn.execute('DROP TABLE IF EXISTS stock_info')
            conn.execute('DROP TABLE IF EXISTS stock_daily')
            
            # Create stock_info table
            conn.execute('''
                CREATE TABLE stock_info (
                    symbol TEXT PRIMARY KEY,
                    name TEXT,
                    full_name TEXT,
                    exchange TEXT,
                    market TEXT,
                    type TEXT,
                    status TEXT,
                    list_date TEXT,
                    delist_date TEXT,
                    industry TEXT,
                    is_hs BOOLEAN
                )
            ''')
            
            # Create stock_daily table
            conn.execute('''
                CREATE TABLE stock_daily (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    trade_date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL,
                    amount REAL,
                    pre_close REAL,
                    adj_factor REAL,
                    FOREIGN KEY(symbol) REFERENCES stock_info(symbol)
                )
            ''')
            
            return True
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        return False
