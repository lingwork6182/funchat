# -*- coding:utf-8 -*-
from src.app.services.UserCurd import UserCurd


async def user_info(user_id: str):
    """
    获取用户信息
    :param user_id:
    :return:
    """
    user_data = await UserCurd.get_user(user_id=user_id)
    if not user_data:
        return {'code': -1, 'msg': f"用户ID=｛user_id｝不存在", 'data': None}

    return {'code': 200, 'msg': f"用户信息", 'data': user_data}
