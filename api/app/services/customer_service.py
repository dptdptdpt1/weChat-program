# 客服配置服务层
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from fastapi import HTTPException

from app.models.customer_service import CustomerService
from app.schemas.customer_service import CustomerServiceCreate, CustomerServiceUpdate


class CustomerServiceService:
    """客服配置服务类"""
    
    @staticmethod
    def get_config(db: Session) -> CustomerService:
        """
        获取客服配置
        
        如果配置不存在,返回默认配置
        
        Args:
            db: 数据库会话
            
        Returns:
            客服配置对象
        """
        # 获取第一条配置记录
        config = db.query(CustomerService).first()
        
        if not config:
            raise HTTPException(
                status_code=404,
                detail="客服配置不存在,请先初始化配置"
            )
        
        return config
    
    @staticmethod
    def create_config(db: Session, config_data: CustomerServiceCreate) -> CustomerService:
        """
        创建客服配置
        
        Args:
            db: 数据库会话
            config_data: 配置数据
            
        Returns:
            创建的配置对象
        """
        config = CustomerService(
            qr_code_url=config_data.qr_code_url,
            online_time=config_data.online_time,
            updated_at=datetime.utcnow()
        )
        db.add(config)
        db.commit()
        db.refresh(config)
        return config
    
    @staticmethod
    def update_config(
        db: Session, 
        config: CustomerService, 
        config_data: CustomerServiceUpdate
    ) -> CustomerService:
        """
        更新客服配置
        
        Args:
            db: 数据库会话
            config: 配置对象
            config_data: 更新数据
            
        Returns:
            更新后的配置对象
        """
        if config_data.qr_code_url is not None:
            config.qr_code_url = config_data.qr_code_url
        if config_data.online_time is not None:
            config.online_time = config_data.online_time
        
        config.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(config)
        return config
