# 存储全局配置信息，如数据库连接信息、第三方接口的密钥等
DATABASE_URI = 'sqlite:///D:/Project/stock_data.db'
TUSHARE_TOKEN = 'gx03013e909f633ecb66722df66b360f070426613316ebf06ecd3482'


class Config:
    def __init__(self):
        self.DATABASE_URI = DATABASE_URI
        self.TUSHARE_TOKEN = TUSHARE_TOKEN

    def init_app(self, app):
        pass

# 其他配置信息可以根据需要添加的