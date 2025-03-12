from flask import Flask, render_template, jsonify, request
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sqlite3
from gm.api import set_token, history
from rooster.integration.myquantServices import MyQuantService
from rooster.services.stock_data import (
    init_db,
    init_api,
    get_stock_symbols,
    update_stock_info,
    fetch_daily_data,
    fetch_all_daily_data,
    get_stock_info
)

app = Flask(__name__, template_folder='../web/templates')

# Database connection helper
def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stock_data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Get analysis data
    analysis_data = analyze_stock_data()
    
    # Get scheduled task data
    today = datetime.now().strftime("%Y-%m-%d")
    data_file = f"stock_data_{today}.json"
    limit_up_data = []
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            limit_up_data = json.load(f)
    
    return render_template('index.html', 
                         analysis_data=analysis_data.to_dict('records'),
                         limit_up_data=limit_up_data)

# New endpoint to get stock list
@app.route('/api/stocks')
def get_stocks():
    conn = get_db()
    stocks = conn.execute('SELECT * FROM stocks ORDER BY symbol').fetchall()
    conn.close()
    return jsonify([dict(row) for row in stocks])

# New endpoint to get daily data
@app.route('/api/daily-data')
def get_daily_data():
    date = request.args.get('date')
    conn = get_db()
    
    if date:
        query = 'SELECT * FROM daily_data WHERE date = ? ORDER BY date DESC, symbol'
        data = conn.execute(query, (date,)).fetchall()
    else:
        query = 'SELECT * FROM daily_data ORDER BY date DESC, symbol'
        data = conn.execute(query).fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in data])

def analyze_stock_data():
    set_token('cb3ca858dfd6aec54ce4e4a8b9eac460d806baeb')
    myquant_service = MyQuantService(api_key='your_api_key_here')
    stocks = myquant_service.get_symbols(exchange='SHSE,SZSE')
    
    limit_up_data = []
    days_to_check = 4
    days_checked = 0
    i = 0
    
    while days_checked < days_to_check:
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            daily_data = pd.DataFrame()
            
            for symbol in stocks['symbol'].tolist():
                try:
                    symbol_data = history(symbol=symbol,
                                        start_time=date + ' 09:00:00',
                                        end_time=date + ' 16:00:00',
                                        frequency='1d',
                                        fields='symbol,close,high,pre_close',
                                        df=True)
                    if not symbol_data.empty:
                        daily_data = pd.concat([daily_data, symbol_data])
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    continue
            
            i += 1
            
            if len(daily_data) > 0:
                days_checked += 1
            
            if len(daily_data) > 0:
                daily_data = daily_data.merge(stocks[['symbol', 'exchange']], on='symbol')
                daily_data['upper_limit'] = daily_data.apply(
                    lambda row: row['pre_close'] * 1.2 
                    if row['exchange'] in ['SZSE', 'SHSE'] and row['symbol'].startswith(('300','301' '688')) 
                    else row['pre_close'] * 1.1, 
                    axis=1
                )
                daily_data['upper_limit'] = daily_data['upper_limit'].round(2)
                limit_up_count = (daily_data['close'] == daily_data['upper_limit']).sum()
                
                limit_up_data.append({'date': date, 'limit_up_count': limit_up_count})
        except Exception as e:
            print(f"Error processing date {date}: {str(e)}")
    
    return pd.DataFrame(limit_up_data)

if __name__ == '__main__':
    app.run(debug=True)
