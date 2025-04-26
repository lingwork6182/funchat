from src.app.models.Base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户信息表'}
    id = Column(String(32), primary_key=True, comment='用户ID')
    user_name = Column(String(255), unique=True, comment='用户名')
    password_has = Column(String(255), comment='用户密码（哈希）')
    conversations = relationship('ConversationModel', back_populates='user')

    def __repr__(self):
        return f"<User(id='{self.id}', user_name='{self.user_name}')>"