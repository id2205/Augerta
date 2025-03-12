import schedule
import time
import json
from datetime import datetime
import logging
from ..services.stock_data import init_api, get_stock_symbols, fetch_daily_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scheduler.log')
    ]
)
logger = logging.getLogger(__name__)

def test_api_connection():
    """Test API connection by fetching data for SHSE.000001"""
    try:
        logger.info("Testing API connection...")
        today = datetime.now().strftime('%Y-%m-%d')
        data = fetch_daily_data('SHSE.000001', today)
        if data.empty:
            logger.error("API connection test failed: empty data")
            return False
        logger.info("API connection test successful")
        return True
    except Exception as e:
        logger.error(f"API connection test failed: {str(e)}")
        return False

def get_stock_data():
    """Get stock data using shared utilities"""
    if not init_api():
        logger.error("Failed to initialize API")
        return None
        
    if not test_api_connection():
        return None
        
    stocks = get_stock_symbols()
    if stocks.empty:
        logger.error("No stock symbols found")
        return None
        
    today = datetime.now().strftime('%Y-%m-%d')
    data = []
    
    for symbol in stocks['symbol'].tolist():
        daily_data = fetch_daily_data(symbol, today)
        if not daily_data.empty:
            data.append(daily_data)
            
    if not data:
        logger.warning("No data collected")
        return None
        
    return pd.concat(data)

def save_to_file(data):
    """Save data to JSON file"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"stock_data_{today}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data.to_dict(orient='records'), f, ensure_ascii=False, indent=2)
    logger.info(f"Data saved to {filename}")

def job():
    """Main scheduled job"""
    logger.info("Starting scheduled job...")
    data = get_stock_data()
    if data is not None:
        save_to_file(data)

# Schedule job to run every weekday at 10:01
schedule.every().monday.at("10:01").do(job)
schedule.every().tuesday.at("10:01").do(job)
schedule.every().wednesday.at("10:01").do(job)
schedule.every().thursday.at("10:01").do(job)
schedule.every().friday.at("10:01").do(job)

def run_now():
    """Run job immediately for testing"""
    logger.info("Running job immediately...")
    job()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        run_now()
    else:
        while True:
            schedule.run_pending()
            time.sleep(1)
