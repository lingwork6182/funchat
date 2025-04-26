from urllib.parse import quote

from dotenv import load_dotenv
import os

from sqlalchemy.connectors import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

class  DataBaseConfig:
    @staticmethod
    def get_async_engine():
        username = os.getenv("DB_USER")
        password = quote(os.getenv("DB_PASSWORD"))
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_NAME")

        SQLALCHEMY_DATABASE_URL = (
            f"mysql+asyncmy://{username}:{password}@{host}/{database}?charset=utf8mb4"
        )

        return create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=os.getenv("SQL_ECHO", "False").lower() == "true",
            pool_size=int(os.getenv("DB_POOL_SIZE", 20)),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 30)),
            pool_pre_ping=True,
            pool_recycle=3600
        )

        return db_engine