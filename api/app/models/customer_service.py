# 客服配置数据模型
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.utils.database import Base


class CustomerService(Base):
    """
    客服配置表模型
    
    存储客服二维码和在线时间等配置信息
    """
    __tablename__ = "customer_service"
    
    # 主键
    id = Column(Integer, primary_key=True, comment="配置ID")
    
    # 客服信息
    qr_code_url = Column(String(500), nullable=False, comment="客服二维码URL")
    online_time = Column(
        String(100), 
        default="10:00-23:00", 
        nullable=False,
        comment="在线时间"
    )
    
    # 时间戳
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间"
    )
    
    def __repr__(self):
        """字符串表示"""
        return f"<CustomerService(id={self.id}, online_time='{self.online_time}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "qr_code_url": self.qr_code_url,
            "online_time": self.online_time,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
