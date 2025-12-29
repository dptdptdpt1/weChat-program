# 用户相关的 Pydantic 模型
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础模型"""
    open_id: str = Field(..., max_length=100, description="微信OpenID")
    nick_name: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="用户头像URL")


class UserCreate(UserBase):
    """创建用户请求模型"""
    pass


class UserUpdate(BaseModel):
    """更新用户请求模型"""
    nick_name: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="用户头像URL")


class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    last_login_at: datetime = Field(..., description="最后登录时间")
    
    class Config:
        from_attributes = True


class WxLoginRequest(BaseModel):
    """微信登录请求模型"""
    code: str = Field(..., min_length=1, description="微信登录凭证code")
    nick_name: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="用户头像URL")
