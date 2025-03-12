from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_engine.db_client import DBClient
from stock_data_system.config.settings import Config
from service.api.stock_router import router as stock_router

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由
app.include_router(stock_router, prefix="/api/v1", tags=["stock"])

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    db_client = DBClient(Config())
    db_client.init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)