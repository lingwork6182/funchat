from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship

from src.app.models.Base import Base


class Message(Base):
    __table_args__ = {'comment': '聊天信息表'}
    id = Column(String(32), primary_key=True, comment='聊天记录ID')
    conversation_id = Column(String(32), ForeignKey('conversation.id'), comment='会话ID')
    chat_type = Column(String(50), comment='聊天类型')
    query = Column(String(4096), comment='用户问题')
    response = Column(String(4096), comment='模型回答')
    meta_data = Column(JSON, default={}, comment='RAG知识库信息')
    feedback_score = Column(Integer, default=-1, comment='用户评分')
    feedback_reason = Column(String(255), default="", comment='用户评分理由')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    conversation = relationship("Conversation", back_populates='messages')
    def __repr__(self):
        return (f"<Message(id='{self.id}', "
                f"chat_type='{self.chat_type}', "
                f"query='{self.query}', "
                f"response='{self.response}', "
                f"meta_data='{self.meta_data}', "
                f"feedback_score='{self.feedback_score}', "
                f"feedback_reason='{self.feedback_reason}', "
                f"create_time='{self.create_time}')>")
