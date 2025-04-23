import pytest

from src.app.repositories.crud_demo import UserDao


@pytest.mark.asyncio
async def test_create_user(test_session):
    """测试用户创建流程"""
    test_data = {
        "username": "test_user",
        "password_hash": "secure_hash_123"
    }

    # 执行创建操作
    created_user = await UserDao.create_user(test_data)

    # 验证结果
    assert created_user.id is not None
    assert created_user.username == test_data["username"]

    # 验证数据库记录
    retrieved_user = await UserDao.get_user(created_user.id)
    assert retrieved_user.username == test_data["username"]


@pytest.mark.asyncio
async def test_delete_user(test_session):
    """测试用户删除流程"""
    # 先创建测试用户
    test_user = await UserDao.create_user({
        "username": "temp_user",
        "password_hash": "temp_hash"
    })

    # 执行删除操作
    result = await UserDao.delete_user(test_user.id)

    # 验证结果
    assert result is True
    deleted_user = await UserDao.get_user(test_user.id)
    assert deleted_user is None