from sqlalchemy import create_engine
import sqlite3
import logging
from .config import CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
