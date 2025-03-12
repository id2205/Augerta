import sqlite3
import pandas as pd
import json
import os
from datetime import datetime
import schedule
import time
from rooster.services.stock_data import init_api, get_stock_symbols, fetch_all_daily_data

# API configuration
API_TOKEN = 'cb3ca858dfd6aec54ce4e4a8b9eac460d806baeb'

# Database setup
DB_FILE = 'rooster/stock_data.db'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create stock info table
    c.execute('''CREATE TABLE IF NOT EXISTS stocks
                 (symbol TEXT PRIMARY KEY,
                  name TEXT,
                  exchange TEXT,
                  industry TEXT,
                  listing_date TEXT)''')
    
    # Create daily market data table
    c.execute('''CREATE TABLE IF NOT EXISTS daily_data
                 (date TEXT,
                  symbol TEXT,
                  open REAL,
                  high REAL,
                  low REAL,
                  close REAL,
                  volume REAL,
                  PRIMARY KEY (date, symbol))''')
    
    conn.commit()
    conn.close()

def fetch_stock_info():
    """Fetch basic stock information"""
    if not init_api():
        return pd.DataFrame()
    return get_stock_symbols()

def fetch_daily_market_data():
    """Fetch daily market data for all stocks"""
    return fetch_all_daily_data()

def save_to_db(stock_info, market_data):
    """Save data to SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    
    # Save stock info
    stock_info.to_sql('stocks', conn, if_exists='replace', index=False)
    
    # Save daily market data
    market_data.to_sql('daily_data', conn, if_exists='append', index=False)
    
    conn.close()

def export_daily_snapshot(market_data):
    """Export daily data as JSON"""
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"daily_snapshot_{today}.json"
    market_data.to_json(filename, orient='records', force_ascii=False)

def append_to_history(market_data):
    """Append to historical CSV"""
    filename = "historical_data.csv"
    market_data.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)

def daily_job():
    """Main job to run daily"""
    print("Starting daily data collection...")
    print(f"Using API token: {API_TOKEN[:4]}...{API_TOKEN[-4:]}")
    
    # Initialize database
    init_db()
    
    # Fetch data
    stock_info = fetch_stock_info()
    market_data = fetch_daily_market_data()
    
    if not market_data.empty:
        # Save to database
        save_to_db(stock_info, market_data)
        
        # Export daily snapshot
        export_daily_snapshot(market_data)
        
        # Append to historical CSV
        append_to_history(market_data)
        
        print(f"Successfully collected data for {len(market_data)} stocks")
    else:
        print("No data collected")

# Schedule daily job at 16:00 (after market close)
schedule.every().day.at("16:00").do(daily_job)

if __name__ == "__main__":
    # Run immediately for testing
    daily_job()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)
