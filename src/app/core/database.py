import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.app.config.db_config import DataBaseConfig
from src.app.models.Base import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engine = DataBaseConfig.get_async_engine()
        self.async_session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )

    @asynccontextmanager
    async def get_session(self):
        """获取异步数据库会话上下文"""
        session = self.async_session_factory()
        try:
            yield session
            await session.commit()
            logger.debug("Transaction committed successfully")
        except Exception as e:
            await session.rollback()
            logger.error(f"Transaction rolled back due to error: {str(e)}")
            raise
        finally:
            await session.close()

    async def create_tables(self):
        """初始化数据库结构"""
        async with self.engine.begin() as conn:
            logger.info("Creating database tables")
            print(Base.metadata.tables.keys())
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully")


# 初始化数据库管理器
db_manager = DatabaseManager()