import logging
from typing import Dict, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from traitlets import Any

from src.app.core.database import db_manager
from src.app.models.TestMessage import TestMessage
from src.app.models.TestUser import TestUser

logger = logging.getLogger(__name__)


class UserDao:
    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Optional[TestUser]:
        async with db_manager.get_session() as session:
            try:
                new_user = TestUser(**user_data)
                session.add(new_user)
                await session.flush()
                logger.info(f"User created: {new_user.username}")
                return new_user
            except IntegrityError as e:
                logger.error(f"User creation failed: {str(e)}")
                raise ValueError("Username already exists") from e
            except Exception as e:
                logger.error(f"Unexpected error creating user: {str(e)}")
                raise

    @staticmethod
    async def get_user(user_id: str) -> Optional[TestUser]:
        async with db_manager.get_session() as session:
            result = await session.get(TestUser, user_id)
            if not result:
                logger.warning(f"User not fond: {user_id}")

            return result

    @staticmethod
    async def update_user(user_id: str, update_data: Dict[str, Any]) -> Optional[TestUser]:
        async with db_manager.get_session() as session:
            stmt = (
                update(TestUser)
                .where(TestUser.id == user_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            if result.rowcount == 0:
                logger.warning(f"User update failed: {user_id} not found")
                return None
            updated_user = await session.get(TestUser, user_id)
            logger.info(f"User updated: {user_id}")

            return updated_user

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        async with db_manager.get_session() as session:
            stmt = delete(TestUser).where(TestUser.id == user_id)
            result = await session.execute(stmt)
            if result.rowcount == 0:
                logger.warning(f"User deletion failed: {user_id} not found")
                return False
            logger.info(f"User deleted: {user_id}")
            return True


class MessageDao:
    @staticmethod
    async def create_message(message_data: Dict[str, Any]) -> TestMessage:
        async with db_manager.get_session() as session:
            try:
                new_message = TestMessage(**message_data)
                session.add(new_message)
                await session.flush()
                logger.info(f"Message created for user: {message_data['user_id']}")
                return new_message
            except Exception as e:
                logger.error(f"Message creation failed: {str(e)}")
                raise
