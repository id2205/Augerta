import os
from pathlib import Path
import logging  # 新增logging模块导入

# 新增项目根目录定义
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Config:
    # Tushare配置
    TUSHARE_TOKEN = 'gx03013e909f633ecb66722df66b360f070426613316ebf06ecd3482'  # 请替换为正确的Tushare Token
    
    # 数据库配置
    DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'stock_data.db')
    
    # 日志配置
    LOG_DIR = BASE_DIR / 'logs'
    LOG_LEVEL = 'INFO'
    
    def init_app(self, app):
        # 确保日志目录存在
        self.LOG_DIR.mkdir(exist_ok=True, parents=True)
        # 配置日志处理器
        logging.basicConfig(
            level=self.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.LOG_DIR / 'stock_system.log'),
                logging.StreamHandler()
            ]
        )

class DevelopmentConfig(Config):
    LOG_LEVEL = 'INFO'

class ProductionConfig(Config):
    pass