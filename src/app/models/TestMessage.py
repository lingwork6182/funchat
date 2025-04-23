from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.app.models.Base import Base

class TestMessage(Base):
    __table_args__ = {'comment': '用户聊天记录表'}
    #id = Column(String(32), primary_key=True, comment='记录ID', server_default=text("uuid()"))
    id = Column(Integer, primary_key=True, comment='记录ID', autoincrement=True)
    user_id = Column(Integer, ForeignKey('testuser.id'), nullable=False, index=True, comment='用户ID')
    chat_type = Column(String(50), nullable=False, comment='聊天类型', index=True)
    query = Column(String(4096), nullable=False, comment='用户问题')
    response = Column(String(4096), nullable=False, comment='模型回答')
    metadata_ = Column('meta_data', JSON, default={}, comment='元数据')
    feedback_score = Column(Integer, default=-1, comment='用户评分(-1=未评分)')
    feedback_reason = Column(String(255), default="", comment='评分理由')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    user = relationship("TestUser", back_populates="messages")
