# 赛事数据模型
from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime
from app.utils.database import Base


class Event(Base):
    """
    赛事表模型
    
    存储足球赛事信息,包括标题、日期、图片等
    """
    __tablename__ = "events"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="赛事ID")
    
    # 基本信息
    title = Column(String(200), nullable=False, comment="赛事标题")
    date = Column(Date, nullable=False, index=True, comment="赛事日期")
    content = Column(String(50000), nullable=True, comment="赛事内容(Markdown格式)")
    
    # 自动提取的封面图（从content中的第一张图片）
    cover_image = Column(String(500), nullable=True, comment="封面图URL(自动提取)")
    
    # 统计信息
    view_count = Column(Integer, default=0, nullable=False, comment="浏览量")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False,
        comment="更新时间"
    )
    
    def __repr__(self):
        """字符串表示"""
        return f"<Event(id={self.id}, title='{self.title}', date={self.date})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.isoformat() if self.date else None,
            "content": self.content,
            "cover_image": self.cover_image,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
