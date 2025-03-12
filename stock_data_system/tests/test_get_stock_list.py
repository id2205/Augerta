import sys
import os
import pytest  # 添加这行

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from data_engine.adapters.tushare import TushareAdapter
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 假设这里有一个配置类，包含 Tushare 的 token
class Config:
    TUSHARE_TOKEN = 'your_tushare_token'  # 请替换为正确的 Tushare Token

# 创建配置实例
config = Config()

def test_get_stock_list():
    logging.info("Testing get stock list...")
    tushare_adapter = TushareAdapter(config)  # 传入 config 参数
    try:
        stock_list = tushare_adapter.get_stock_list()
        assert not stock_list.empty, "Failed to get stock list"
        logging.info("Stock list fetched successfully.")
        if not stock_list.empty:
            logging.info("成功获取股票列表：")
            logging.info(stock_list.to_csv(sep='\t', na_rep='nan'))
        else:
            logging.warning("未获取到股票列表。")
    except Exception as e:
        logging.error(f"Failed to get stock list: {e}")
        pytest.fail(f"Test failed: {e}")

# 调用测试函数
test_get_stock_list()