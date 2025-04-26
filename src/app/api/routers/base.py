# -*- coding:utf-8 -*-
from fastapi import APIRouter

from src.app.repositories.user_manager import user_info

ApiRouter = APIRouter(prefix="/v1", tags=["用户管理"])

ApiRouter.get("/user", summary="获取用户信息")(user_info)
