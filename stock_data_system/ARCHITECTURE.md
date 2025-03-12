# 股票数据系统架构说明

## 1. 系统架构设计

**分层架构**：
- **数据采集层**：适配器模式实现数据源解耦
- **存储层**：SQLAlchemy ORM 统一数据访问
- **服务层**：FastAPI 提供 RESTful 接口
- **展示层**：Vue3 + ECharts 实现数据可视化

## 2. 目录结构

```
stock_data_system/
├── config/               # 配置管理
│   ├── __init__.py
│   ├── settings.py       # 全局配置
│   └── logging.conf      # 日志配置
├── data_engine/          # 数据引擎核心
│   ├── adapters/         # 数据源适配器
│   │   ├── tushare.py    # Tushare实现
│   ├── models/           # ORM 模型
│   │   ├── base.py       # 基础模型
│   │   ├── stock.py      # 证券基础信息
│   │   └── trade.py      # 交易数据
│   └── db_client.py      # 数据库客户端
├── service/              # 业务服务
│   ├── api/              # FastAPI 路由
│   ├── scheduler/        # 定时任务
│   └── utils/            # 工具包
├── web/                  # 前端工程
│   ├── public/           # 静态资源
│   ├── src/              # 源码目录
│   │   ├── api/         # 接口定义
│   │   ├── charts/      # ECharts组件
│   │   └── store/       # Pinia状态管理
└── requirements.txt      # 依赖清单
```

## 3. 核心表结构设计

**证券基础信息表 (stock_info)**
```sql
CREATE TABLE stock_info (
    symbol VARCHAR(12) PRIMARY KEY,    -- 证券代码
    name VARCHAR(64),                 -- 证券名称
    exchange VARCHAR(16),             -- 交易所
    industry VARCHAR(32),             -- 所属行业
    list_date DATE,                    -- 上市日期
    status VARCHAR(8)                 -- 上市状态
);
```

**分钟K线表 (minute_kline)**
```sql
CREATE TABLE minute_kline (
    id BIGINT PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(12),               -- 证券代码
    timestamp DATETIME,               -- 时间戳
    open DECIMAL(10,2),               -- 开盘价
    high DECIMAL(10,2),               -- 最高价
    low DECIMAL(10,2),                -- 最低价
    close DECIMAL(10,2),              -- 收盘价
    volume BIGINT,                    -- 成交量
    turnover DECIMAL(16,2),           -- 成交额
    adjust_flag BOOLEAN               -- 复权标记
);
```

## 4. 扩展性设计

1. **数据源适配器接口**：
```python
class DataAdapter(ABC):
    @abstractmethod
    def get_daily_data(self, symbol: str) -> pd.DataFrame: ...
    
    @abstractmethod 
    def get_minute_data(self, symbol: str) -> pd.DataFrame: ...
```

2. **配置驱动切换**：通过修改配置文件的 `data_source` 字段实现热切换

3. **统一数据格式**：所有适配器输出统一数据结构的 DataFrame