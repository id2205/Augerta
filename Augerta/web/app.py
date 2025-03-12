# 导入必要的库
from flask import Flask, jsonify
import pandas as pd
from Augerta.data_engine.db_client import DatabaseClient
from Augerta.data_engine.models import Stock, DailyData, MinuteQuote
from Augerta.config.settings import Config
from Augerta.data_engine.models import ThsMember, ThsIndex
from sqlalchemy.orm import sessionmaker
from Augerta.data_engine.db_client import DatabaseClient
from Augerta.config.settings import Config

app = Flask(__name__)

# 初始化数据库客户端
config = Config()
config.init_app(None)
db_client = DatabaseClient(config)

# 定义路由，展示股票和指数数据
@app.route('/')
def index():
    # 获取股票列表
    stock_list = db_client.get_session().query(Stock).all()
    # 获取日线数据
    daily_data = db_client.get_session().query(DailyData).all()
    # 获取分钟线数据
    minute_data = db_client.get_session().query(MinuteQuote).all()
    
    # 将数据转换为DataFrame
    stock_df = pd.DataFrame([stock.__dict__ for stock in stock_list])
    daily_df = pd.DataFrame([data.__dict__ for data in daily_data])
    minute_df = pd.DataFrame([data.__dict__ for data in minute_data])
    
    # 生成HTML表格
    stock_table = stock_df.to_html()
    daily_table = daily_df.to_html()
    minute_table = minute_df.to_html()
    
    # 组合HTML页面
    html = f'<h1>股票数据</h1>{stock_table}<h1>日线数据</h1>{daily_table}<h1>分钟线数据</h1>{minute_table}'
    
    return html

@app.route('/stocks')
def stock_list():
    stock_list = db_client.get_session().query(Stock).all()
    stock_links = [f'<a href="/daily/{stock.ts_code}">{stock.name}</a>' for stock in stock_list]
    stock_html = '<br>'.join(stock_links)
    return f'<h1>股票列表</h1>{stock_html}'

@app.route('/daily/<string:ts_code>')
def daily_data(ts_code):
    daily_data = db_client.get_session().query(DailyData).filter(DailyData.ts_code == ts_code).all()
    import plotly.graph_objects as go
    import pandas as pd
    df = pd.DataFrame([data.__dict__ for data in daily_data])
    fig = go.Figure(data=[go.Candlestick(x=df['trade_date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    fig.update_layout(title='K线图', yaxis_title='价格')
    plot_div = fig.to_html(full_html=False)
    return f'<h1>日线数据</h1>{plot_div}'

@app.route('/call_auction/<string:date>')
def call_auction(date):
    from Augerta.web.src.api.call_auction_api import get_call_auction_data
    from Augerta.web.src.store.call_auction_store import process_call_auction_data
    print(date)
    data = get_call_auction_data(date)
    if data is None:
        return jsonify({'message': f'暂无 {date} 的竞价涨停数据'}), 404
    df = process_call_auction_data(data)
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)