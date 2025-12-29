# 用户数据模型
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.utils.database import Base


class User(Base):
    """
    用户表模型
    
    存储微信小程序用户信息
    """
    __tablename__ = "users"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    
    # 微信信息
    open_id = Column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True, 
        comment="微信OpenID"
    )
    
    # 用户信息
    nick_name = Column(String(100), comment="用户昵称")
    avatar_url = Column(String(500), comment="用户头像URL")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    last_login_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False,
        comment="最后登录时间"
    )
    
    def __repr__(self):
        """字符串表示"""
        return f"<User(id={self.id}, open_id='{self.open_id}', nick_name='{self.nick_name}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "open_id": self.open_id,
            "nick_name": self.nick_name,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }
