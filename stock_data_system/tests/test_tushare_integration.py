import sys
import os
import logging  # 导入 logging 模块
import pdb  # 新增：导入 pdb 模块

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.insert(0, project_root)

# 调试信息：打印 sys.path
logging.info("sys.path: %s", sys.path)

import pytest
from pathlib import Path
from unittest.mock import patch
import pandas as pd  # 添加这行
from data_engine.adapters.tushare import TushareAdapter
from config.settings import Config, DevelopmentConfig
from data_engine.db_client import DatabaseClient

@pytest.fixture
def test_config():
    class TestConfig(DevelopmentConfig):
        DATABASE_URI = 'sqlite:///:memory:'
    return TestConfig

@pytest.fixture
def db_client(test_config):
    client = DatabaseClient(test_config)
    client.initialize()
    logging.info("Database client initialized.")
    yield client
    client.session.close()
    logging.info("Database client session closed.")

@pytest.fixture
def tushare_adapter(test_config):
    adapter = TushareAdapter(test_config)
    logging.info("Tushare adapter initialized with config: %s", test_config)
    return adapter

def test_tushare_config_loading(tushare_adapter):
    logging.info("Testing Tushare config loading...")
    assert hasattr(tushare_adapter.config, 'TUSHARE_TOKEN')
    # 更新长度断言
    assert len(tushare_adapter.config.TUSHARE_TOKEN) == 56
    logging.info("Tushare config loading test passed.")

import pytest
import logging

# 假设从正确的模块导入 TushareAdapter
from data_engine.adapters.tushare import TushareAdapter

# 修改函数名以反映测试的是日线数据
def test_daily_data_fetching(test_config):
    logging.info("Testing daily data fetching...")
    tushare_adapter = TushareAdapter(test_config)

    try:
        # 修改为调用获取日线数据的方法
        result = tushare_adapter.get_daily_data('600000.SH')
        logging.info("Daily data fetched: %s", result)

        # 检查 result 是否为空
        if result.empty:
            logging.warning("获取到的日线数据为空")
        else:
            # 输出获取到的数据
            logging.info("获取到的日线数据：\n%s", result.to_csv(sep='\t', na_rep='nan'))
    
            # 新增：将数据保存到本地 CSV 文件
            csv_file_path = 'daily_stock_data.csv'
            result.to_csv(csv_file_path, index=False, encoding='utf-8-sig')  # 指定编码为 UTF-8 with BOM
            logging.info(f"日线数据已保存到 {csv_file_path}")

        # 验证字段映射
        assert 'date' in result.columns  # 修改为验证 'date' 列
        assert 'open' in result.columns
        # 验证关键数值字段存在
        assert all(col in result.columns for col in ['open', 'high', 'low', 'close', 'volume'])
        logging.info("Daily data fetching test passed.")
    except Exception as e:
        logging.error(f"Failed to fetch daily data: {e}")
        raise



def test_get_stock_list(test_config):
    logging.info("Testing get stock list...")
    tushare_adapter = TushareAdapter(test_config)
    try:
        stock_list = tushare_adapter.get_stock_list()
        assert not stock_list.empty, "Failed to get stock list"

        if not stock_list.empty:
            logging.info("成功获取股票列表：")
            logging.info(stock_list.to_csv(sep='\t', na_rep='nan'))

            # 保存股票列表到 CSV 文件，指定编码为 utf-8-sig
            csv_file_path = 'stock_list.csv'
            stock_list.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
            logging.info(f"股票列表已保存到 {csv_file_path}")
        else:
            logging.warning("未获取到股票列表。")
    except Exception as e:
        logging.error(f"Failed to get stock list: {e}")
        pytest.fail(f"Test failed: {e}")

# 删除手动调用语句
# test_get_stock_list()