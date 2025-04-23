import asyncio
import logging

from src.app.core.database import db_manager
from src.app.repositories.crud_demo import UserDao, MessageDao

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s -%(message)s"
)


async def main():
    #数据库初始化
    await db_manager.create_tables()

    # # 测试用户操作
    # try:
    #     # 创建用户
    #     new_user = await UserDao.create_user({"username": "xxx3", "password_hash": "123456"})
    #     print(f"Created user: {new_user.username}")
    #
    #     #查询用户
    #     user = await UserDao.get_user(new_user.id)
    #     print(f"Retrieved user: {user.username}")
    #     #
    #     #更新用户
    #     updated_user = await UserDao.update_user(
    #         user.id,
    #         {"username": "updated_enterprise_user"}
    #     )
    #     print(f"Updated username: {updated_user.username}")
    #
    #     # 创建消息
    #     message = await MessageDao.create_message({
    #         "user_id": user.id,
    #         "chat_type": "support",
    #         "query": "How to reset password?",
    #         "response": "Please visit our password reset page..."
    #     })
    #     print(f"Created message ID: {message.id}")
    #
    #     # 删除用户
    #     success = await UserDao.delete_user(user.id)
    #     print(f"Delete successful: {success}")
    #
    # except Exception as e:
    #     logging.error(f"Main execution failed: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
