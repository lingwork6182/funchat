# -*- coding:utf-8 -*-

import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    #加载环境变量
    load_dotenv(find_dotenv(), override=True)

    #调试模式
    APP_DEBUG: bool = True

    #项目信息
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "FunAIchat"
    DESCRIPTION: str = "智能知识库"

    # #静态资源目录
    # STATIC_DIR: str = os.path.join(os.getcwd(), "app/static")
    # TEMPLATES_DIR: str = os.path.join(STATIC_DIR, "templates")
    #
    # #跨域请求
    # CORS_ORIGINS: List = ["*"]
    # CORS_ALLOW_CREDENTIALS: bool = True
    # CORS_ALLOW_METHODS: List = ["*"]
    # CORS_ALLOW_HEADERS: List = ["*"]
    #
    # #Session
    # SECRET_KEY: str = 'session'  #服务端存储
    # SESSION_COOKIE: str = 'session_id' #客户端存储
    # SESSION_MAX_AGE: int = 14 * 24 * 60 * 60  #会话失效时间：14天
    #
    # #jwt -> java script web token 一种认证的协议
    # JWT_SECRET_KEY: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    # JWT_ALGORITHM: str = 'HS256'
    # JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60


app_settings = Config()

