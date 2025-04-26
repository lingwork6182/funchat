import asyncio

from src.app.services.UserCurd import UserCurd


async def create_user_test():
    test_data = {
        "id": "100000004",
        "user_name": "zhaoliu",
        "password_has": "123456"
    }

    new_user = await UserCurd.create_user(test_data)
    print(f"new_user={new_user}")

    # 验证结果
    #assert new_user.id is not None
    #assert new_user.user_name == test_data["user_name"]

    # 验证数据库记录
    # retrieved_user = await UserCurd.get_user(new_user.id)
    # assert retrieved_user.username == test_data["username"]

async def get_userinfo():
    userinfo = await UserCurd.get_user('100000004')
    print(userinfo)

async def update_userinfo():
    new_userinfo ={
        "user_name": "xiaoliu3"
    }

    userinfo = await UserCurd.update_user('100000004', new_userinfo)
    print(userinfo)
async def delete_userbyid():
    res = await UserCurd.delete_user('100000004')
    print(res)


if __name__ == '__main__':
    asyncio.run(delete_userbyid())

