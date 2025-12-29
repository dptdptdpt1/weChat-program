# 客服配置相关的 Pydantic 模型
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CustomerServiceBase(BaseModel):
    """客服配置基础模型"""
    qr_code_url: str = Field(..., max_length=500, description="客服二维码URL")
    online_time: str = Field(default="10:00-23:00", max_length=100, description="在线时间")


class CustomerServiceCreate(CustomerServiceBase):
    """创建客服配置请求模型"""
    pass


class CustomerServiceUpdate(BaseModel):
    """更新客服配置请求模型"""
    qr_code_url: Optional[str] = Field(None, max_length=500, description="客服二维码URL")
    online_time: Optional[str] = Field(None, max_length=100, description="在线时间")


class CustomerServiceResponse(CustomerServiceBase):
    """客服配置响应模型"""
    id: int = Field(..., description="配置ID")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
