import asyncio
import logging

from src.app.core.database import db_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s -%(message)s"
)

#数据库初始化
async def init_database():
    await db_manager.create_tables()


if __name__ == '__main__':
    asyncio.run(init_database())