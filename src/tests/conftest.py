import pytest

from src.app.core.database import db_manager


@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    await db_manager.create_tables()
    yield
    await db_manager.engine.dispose()