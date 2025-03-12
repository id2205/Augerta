import pandas as pd
from datetime import datetime
import os
import sqlite3
from gm.api import set_token, history
from rooster.integration.myquantServices import MyQuantService
import logging
from sqlalchemy import create_engine
from rooster.storage.initdb import init_db
from rooster.config import API_CONFIG

# Create database engine
DB_ENGINE = create_engine('sqlite:///rooster/stock_data.db')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# API Token setup
API_TOKEN = API_CONFIG['GM_API_TOKEN']

def init_api():
    """Initialize API connection"""
    set_token(API_TOKEN)
    return True

def get_stock_symbols(exchange='SHSE,SZSE', save_to_file=True):
    """Get stock symbols from MyQuant API"""
    api_key = API_CONFIG['GM_API_TOKEN']
    if not api_key:
        logger.debug('GM_API_TOKEN environment variable not set')
        return pd.DataFrame()

    service = MyQuantService(api_key=api_key)
    
    # Try up to 3 times
    for attempt in range(3):
        try:
            symbols = service.get_symbols(exchange=exchange)
            if symbols is not None:
                if save_to_file:
                    # Ensure directory exists and has proper permissions
                    os.makedirs('rooster', exist_ok=True)
                    # Save raw data with proper file permissions
                    symbols.to_csv('rooster/raw_stock_data.csv', index=False, mode='w')
                    # Set file permissions to allow read/write
                    os.chmod('rooster/raw_stock_data.csv', 0o666)
                return symbols
        except Exception as e:
            logger.debug(f'Error fetching stock symbols (attempts left: {2 - attempt}): {str(e)}')
            if attempt == 2:
                logger.debug('Failed to fetch stock symbols after 3 attempts')
                return pd.DataFrame()

def update_stock_info():
    """Update stock information in database"""
    logger.debug("Starting stock info update")
    
    stocks = get_stock_symbols()
    
    if stocks.empty:
        logger.debug("No stock data received from API")
        return False
    
    logger.debug(f"Received {len(stocks)} stock records")
    
    try:
        with DB_ENGINE.connect() as conn:
            logger.debug("Updating stock info in database")
            stocks.to_sql('stock_info', conn, if_exists='replace', index=False)
            logger.debug("Stock info update completed successfully")
            return True
    except Exception as e:
        logger.debug(f"Error updating stock info: {str(e)}", exc_info=True)
        return False

def fetch_daily_data(symbol, date):
    """Fetch daily market data for a single stock"""
    retries = 3
    while retries > 0:
        try:
            data = history(
                symbol=symbol,
                start_time=date + ' 09:30:00',
                end_time=date + ' 15:00:00',
                frequency='1d',
                fields='symbol,open,high,low,close,volume',
                df=True
            )
            if not data.empty:
                return data
            retries -= 1
        except Exception as e:
            retries -= 1
            if retries == 0:
                logger.debug(f"Failed to fetch data for {symbol}: {str(e)}")
    return pd.DataFrame()

def fetch_all_daily_data():
    """Fetch daily market data for all stocks"""
    today = datetime.now().strftime('%Y-%m-%d')
    stocks = get_stock_symbols()
    
    if stocks.empty:
        return pd.DataFrame()
    
    data = []
    failed_symbols = []
    
    for symbol in stocks['symbol'].tolist():
        daily_data = fetch_daily_data(symbol, today)
        if not daily_data.empty:
            data.append(daily_data)
        else:
            failed_symbols.append(symbol)
    
    if failed_symbols:
        logger.debug(f"Failed to fetch data for {len(failed_symbols)} symbols")
    
    return pd.concat(data) if data else pd.DataFrame()

def get_stock_info(symbol=None):
    """Get stock information from database"""
    query = "SELECT symbol, name, exchange, industry, list_date FROM stock_info"
    if symbol:
        query += f" WHERE symbol = '{symbol}'"
    query += " LIMIT 5"
    
    try:
        with DB_ENGINE.connect() as conn:
            df = pd.read_sql_query(query, conn)
            
            # Write query results to file
            output_file = 'rooster/stock_info_output.txt'
            with open(output_file, 'w') as f:
                if not df.empty:
                    f.write("Stock info query results:\n")
                    f.write(df.to_string(index=False))
                else:
                    f.write("No stock info found")
            
            return df
    except Exception as e:
        logger.debug(f"Database query error: {str(e)}")
        return pd.DataFrame()
