# -*- coding:utf-8 -*-
from fastapi import APIRouter

from src.app.api.routers.base import ApiRouter


#总路由
AllRouter = APIRouter()

#用户管理模块
AllRouter.include_router(ApiRouter)