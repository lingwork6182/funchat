#添加连接测试方法
import pytest

from src.app.config.db_config import DataBaseConfig


@pytest.mark.asyncio
async def test_connection():
    try:
        async with DataBaseConfig.get_async_engine().connect() as conn:
            print("Database connection successful!")
    except Exception as e:
        print(f"Connection failed: {str(e)}")