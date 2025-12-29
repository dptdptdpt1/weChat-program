# 赛事数据模式
from pydantic import BaseModel, Field
from datetime import date as DateType, datetime as DateTimeType
from typing import Optional


class EventBase(BaseModel):
    """赛事基础模式"""
    title: str = Field(description="赛事标题", min_length=1, max_length=200)
    date: DateType = Field(description="赛事日期")
    content: Optional[str] = Field(None, description="赛事内容(Markdown格式)", max_length=50000)


class EventCreate(EventBase):
    """创建赛事模式"""
    pass


class EventUpdate(BaseModel):
    """更新赛事模式"""
    title: Optional[str] = Field(None, description="赛事标题", min_length=1, max_length=200)
    date: Optional[DateType] = Field(None, description="赛事日期")
    content: Optional[str] = Field(None, description="赛事内容(Markdown格式)", max_length=50000)


class EventResponse(EventBase):
    """赛事响应模式"""
    id: int = Field(description="赛事ID")
    cover_image: Optional[str] = Field(None, description="封面图URL")
    view_count: int = Field(description="浏览量")
    created_at: DateTimeType = Field(description="创建时间")
    updated_at: DateTimeType = Field(description="更新时间")
    
    class Config:
        from_attributes = True


class EventListQuery(BaseModel):
    """赛事列表查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页大小")
    keyword: Optional[str] = Field(None, description="搜索关键词", max_length=100)
