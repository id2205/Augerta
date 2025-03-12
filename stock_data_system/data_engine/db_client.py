from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stock_data_system.config.settings import Config

class DatabaseClient:
    def __init__(self, config: Config):
        self.engine = create_engine(config.DATABASE_URI)
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False)
        
    def initialize(self):
        from ..models.base import Base
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        return self.SessionLocal()

    def execute_query(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            result = conn.execute(query, params or {})
            return result.fetchall()
    def bulk_insert(self, model, records):
        session = self.SessionLocal()
        try:
            session.bulk_insert_mappings(model, records)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()