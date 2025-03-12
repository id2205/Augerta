# Augerta项目架构说明

## 一、项目概述
本项目名为Augerta，主要用于监控A股市场情绪。通过第三方接口实时获取股票数据，并进行分析展示，数据每日和实时更新。

## 二、项目结构

### 1. 目录结构
```
Augerta/
├── config/               # 配置管理
│   ├── __init__.py
│   ├── settings.py       # 全局配置
│   └── logging.conf      # 日志配置
├── data_engine/          # 数据引擎核心
│   ├── adapters/         # 数据源适配器
│   │   ├── tushare.py    # Tushare实现
│   │   └── __init__.py
│   ├── models/           # ORM 模型
│   │   ├── base.py       # 基础模型
│   │   ├── stock.py      # 证券基础信息
│   │   ├── index.py      # 指数信息
│   │   ├── industry.py   # 行业信息
│   │   └── __init__.py
│   └── db_client.py      # 数据库客户端
├── service/              # 业务服务
│   ├── api/              # FastAPI 路由
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── scheduler/        # 定时任务
│   │   ├── __init__.py
│   │   └── tasks.py
│   └── utils/            # 工具包
│       └── __init__.py
├── analysis/             # 数据分析模块
│   ├── __init__.py
│   └── analyzer.py
├── web/                  # 前端工程
│   ├── public/           # 静态资源
│   ├── src/              # 源码目录
│   │   ├── api/         # 接口定义
│   │   ├── charts/      # ECharts组件
│   │   └── store/       # Pinia状态管理
│   └── __init__.py
└── requirements.txt      # 依赖清单
```

### 2. 模块说明

#### 2.1 config模块
- `settings.py`：存储全局配置信息，如数据库连接信息、第三方接口的密钥等。
- `logging.conf`：配置日志记录的格式和级别。

#### 2.2 data_engine模块
- `adapters`：实现不同第三方数据源的适配器，目前包含Tushare适配器，未来可扩展其他数据源。
- `models`：定义数据库表结构，使用ORM框架（如SQLAlchemy）进行数据库操作。
- `db_client.py`：负责与数据库建立连接，提供数据存储和查询的接口。

#### 2.3 service模块
- `api`：使用FastAPI构建RESTful API，提供数据查询和分析结果的接口。
- `scheduler`：使用定时任务框架（如APScheduler）实现数据的每日和实时更新。
- `utils`：提供一些通用的工具函数。

#### 2.4 analysis模块
- `analyzer.py`：对获取的数据进行分析，如竞价阶段表现、整点表现、收盘后涨跌情况等。

#### 2.5 web模块
- 前端工程，使用现代前端框架（如Vue.js）构建用户界面，展示分析结果。

## 三、数据获取与存储

### 1. 数据获取
- 通过Tushare的pro接口获取股票数据，代码示例如下：
```python
import tushare as ts

# 初始化pro接口
def get_pro_api(token):
    return ts.pro_api(token)

# 示例：获取沪深A股指数日线行情
def get_index_daily(pro, index_code, start_date, end_date):
    return pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)
```

### 2. 数据存储
- 使用SQLite数据库存储数据，数据库表结构参考Tushare的数据结构，确保符合范式规范。示例代码如下：
```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String)
    symbol = Column(String)
    name = Column(String)
    area = Column(String)
    industry = Column(String)
    # 其他字段...

engine = create_engine('sqlite:///stock_data.db')
Base.metadata.create_all(engine)
```

## 四、扩展性设计

### 1. 数据源适配器接口
```python
from abc import ABC, abstractmethod
import pandas as pd

class DataAdapter(ABC):
    @abstractmethod
    def get_index_info(self) -> pd.DataFrame: ...

    @abstractmethod
    def get_index_daily(self, index_code: str, start_date: str, end_date: str) -> pd.DataFrame: ...

    @abstractmethod
    def get_stock_basic(self) -> pd.DataFrame: ...

    @abstractmethod
    def get_stock_daily(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame: ...

    @abstractmethod
    def get_stock_minute(self, stock_code: str, start_time: str, end_time: str) -> pd.DataFrame: ...
```

### 2. 配置驱动切换
通过修改配置文件的 `data_source` 字段实现热切换第三方数据源。

### 3. 统一数据格式
所有适配器输出统一数据结构的DataFrame，方便后续分析和处理。

## 五、数据分析与展示

### 1. 数据分析
在 `analysis` 模块中实现各种分析逻辑，例如：
```python
import pandas as pd

# 分析竞价阶段表现
def analyze_call_auction(data):
    # 实现分析逻辑
    return result

# 分析每个整点表现
def analyze_hourly_performance(data):
    # 实现分析逻辑
    return result

# 分析收盘后市场股票上涨下跌情况
def analyze_closing_market(data):
    # 实现分析逻辑
    return result
```

### 2. 数据展示
使用前端框架（如Vue.js）和ECharts组件，将分析结果以图表的形式展示给用户。

## 六、开发计划

### 1. 第一阶段：项目初始化和数据获取
- 创建项目目录结构
- 实现Tushare数据源适配器
- 设计数据库表结构并实现数据存储

### 2. 第二阶段：数据分析和展示
- 实现数据分析逻辑
- 构建前端界面，展示分析结果

### 3. 第三阶段：扩展性和优化
- 实现数据源切换接口
- 优化代码性能和稳定性