# -*- coding:utf-8 -*-

from sqlalchemy.orm import DeclarativeBase


#创建一个基类，用于定义数据模型的基本结构
# class Base(AsyncAttrs, DeclarativeBase):
#     @declared_attr.directive
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
class Base(DeclarativeBase):
    pass
