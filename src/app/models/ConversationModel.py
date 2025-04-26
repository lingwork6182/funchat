from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship

from src.app.models.Base import Base
class ConversationModel(Base):
    __tablename__ = 'conversation'
    __table_args__ = {'comment': '会话信息表'}
    id = Column(String(32), primary_key=True, comment='会话ID')
    user_id = Column(String(32), ForeignKey('user.id'), comment='用户ID')
    name = Column(String(50), comment='对话框名称')
    chat_type = Column(String(50), comment='聊天类型')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    # 会话与用户的多对一关系
    user = relationship('UserModel', back_populates='conversations')
    # 会话与消息的一对多关系
    messages = relationship('MessageModel', back_populates='conversations')
    def __repr__(self):
        return (f"<Conversation(id='{self.id}'>, name='{self.name}', chat_type='{self.chat_type}', create_time='{self.create_time}')>")