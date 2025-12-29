# 上传图片记录模型
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.utils.database import Base


class UploadedImage(Base):
    """
    上传图片记录表
    
    记录所有上传的图片，方便管理和引用
    """
    __tablename__ = "uploaded_images"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="图片ID")
    
    # 图片信息
    filename = Column(String(200), nullable=False, comment="文件名")
    url = Column(String(500), nullable=False, comment="访问URL")
    size = Column(Integer, nullable=False, comment="文件大小(字节)")
    type = Column(String(50), nullable=False, comment="图片类型(event/thumbnail)")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="上传时间")
    
    def __repr__(self):
        """字符串表示"""
        return f"<UploadedImage(id={self.id}, filename='{self.filename}')>"
    
    @property
    def markdown_syntax(self):
        """返回 Markdown 语法"""
        return f"![图片]({self.url})"
    
    @property
    def size_kb(self):
        """返回文件大小(KB)"""
        return round(self.size / 1024, 2)
