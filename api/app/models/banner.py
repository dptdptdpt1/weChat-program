# 顶部滚动栏模型
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.utils.database import Base


class Banner(Base):
    """
    顶部滚动栏表
    
    用于管理首页顶部的轮播图
    """
    __tablename__ = "banners"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="轮播图ID")
    
    # 图片信息
    image_url = Column(String(500), nullable=False, comment="图片URL")
    title = Column(String(200), nullable=True, comment="标题（可选）")
    link_url = Column(String(500), nullable=True, comment="跳转链接（可选）")
    
    # 排序和状态
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序（数字越小越靠前）")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    def __repr__(self):
        """字符串表示"""
        return f"<Banner(id={self.id}, title='{self.title}', sort_order={self.sort_order})>"
