from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_engine.db_client import DBClient
from config.settings import Config
from data_engine.models.stock import Stock
from data_engine.models.trade import MinuteKline

router = APIRouter()

def get_db():
    client = DBClient(Config())
    return client.get_session()

@router.get("/stocks")
async def get_stocks(db: Session = Depends(get_db)):
    return db.query(Stock).limit(100).all()

@router.get("/minute/{symbol}")
async def get_minute_data(symbol: str, db: Session = Depends(get_db)):
    return db.query(MinuteKline).filter(MinuteKline.symbol == symbol).order_by(MinuteKline.timestamp.desc()).limit(240).all()