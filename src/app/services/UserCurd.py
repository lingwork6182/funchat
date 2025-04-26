import logging
from typing import Dict, Optional, Any

from sqlalchemy import update, delete

from src.app.core.database import db_manager
from src.app.models import UserModel

logger = logging.getLogger(__name__)
class UserCurd:
    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Optional[UserModel]:
        async with db_manager.get_session() as session:
            try:
                new_user = UserModel(**user_data)
                session.add(new_user)
                await session.flush()
                logger.info(f"User created: {new_user.user_name}")
            except InterruptedError as e:
                logger.error(f"User creation failed: {str(e)}")
                raise ValueError("Username alread exsits") from e
            except ValueError as e:
                logger.error(f"Unexpected error create user: {str(e)}")
                raise

    async def get_user(user_id: str) -> Optional[UserModel]:
        async with db_manager.get_session() as session:
            result = await  session.get(UserModel, user_id)

            if not result:
                logger.warning(f"User not fond: {user_id}")

            return result


    async def update_user(user_id: str, update_data: Dict[str, Any]) -> Optional[UserModel]:
        async with db_manager.get_session() as sesion:
            stmt = (update(UserModel)
                    .where(UserModel.id == user_id)
                    .values(**update_data)
                    .execution_options(synchronize_session="fetch")
                    )

            result = await sesion.execute(stmt)
            #print(type(result))
            if result.rowcount == 0:
                logger.warning(f"User update failed: {user_id} not found")
                return None
            update_user = await sesion.get(UserModel, user_id)
            logger.info(f"User updated: {user_id}")

            return update_user

    async def delete_user(user_id: str) -> bool:
        async with db_manager.get_session() as session:
            stmt = delete(UserModel).where(UserModel.id == user_id)
            result = await session.execute(stmt)
            if result.rowcount == 0:
                logger.warning(f"User deletion failed: {user_id} not found")
                raise False
            logger.info(f"User deleted: {user_id}")

            return True
