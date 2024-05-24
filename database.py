import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_size=20,
            max_overflow=50,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=False,
        )
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def get_engine(self):
        return self.engine
