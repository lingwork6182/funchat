import logging
from typing import Optional

from src.app.models.Base import User
from src.app.repositories.crud_demo import UserDao

logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    async def create_user(cls, user_data: dict) -> Optional[User]:
        """业务逻辑层用户创建"""
        try:
            # 添加业务校验逻辑
            if len(user_data.get("password", "")) < 8:
                raise ValueError("Password too short")

            return await UserDao.create_user(user_data)
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}")
            raise