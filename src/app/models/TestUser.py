from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.app.models.Base import Base


class TestUser(Base):
    __table_args__ = {'comment': '用户信息表'}
    #id = Column(String(64), primary_key=True, comment='用户ID', server_default=text("uuid()"))
    id = Column(Integer, primary_key=True, comment='用户ID', autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, comment='用户名', index=True)
    password_hash = Column(String(255), nullable=False, comment='密码哈希值')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    #定义关系，与 Message 类的关系为多对多关系，通过 back_populates 指定反向关系属性名
    messages = relationship("TestMessage", back_populates="user", cascade="all, delete-orphan")
