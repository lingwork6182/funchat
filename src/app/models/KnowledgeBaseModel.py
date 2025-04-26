# -*- coding:utf-8 -*-
"""
@NAME: KnowledgeBaseModel.py
@Auth: ASUS
@Date: 2025/4/25
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, func, ForeignKey
from sqlalchemy.orm import relationship

from src.app.models.Base import Base


class KnowledgeBaseModel(Base):
    __tablename__ = '知识库模型'
    __table_args__ = {'comment': 'knowledge_base'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='知识库ID')
    kb_name = Column(String(50), comment='知识库名称')
    kb_info = Column(String(255), comment='知识库简介（用于Agent）')
    vs_type = Column(String(50), comment='向量库类型')
    embed_model = Column(String(50), comment='嵌入模型名称')
    file_count = Column(Integer, default=0, comment='文件数量')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    user_id = Column(String(32), ForeignKey('user.id'), nullable=False, comment='用户ID')

    user = relationship("UserModel", back_populates='knowledge_bases')


    def __repr__(self):
        return (f"<KnowledgeBase(id='{self.id}', kb_name='{self.kb_name}', kb_info='{self.kb_info}', "
                f"vs_type='{self.vs_type}', embed_model='{self.embed_model}', file_count='{self.file_count}', "
                f"create_time='{self.create_time}', user_id='{self.user_id}')>")

