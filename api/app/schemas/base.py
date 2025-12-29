# 基础响应模型
from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel

# 泛型类型变量
T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一 API 响应格式
    
    Attributes:
        code: 状态码 (200 表示成功)
        message: 响应消息
        data: 响应数据
    """
    code: int
    message: str
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "操作成功",
                "data": None
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    分页响应模型
    
    Attributes:
        items: 数据项列表
        total: 总数据量
        page: 当前页码
        page_size: 每页大小
        has_more: 是否有更多数据
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    has_more: bool

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": 10,
                "has_more": False
            }
        }


class ErrorDetail(BaseModel):
    """
    错误详情模型
    
    Attributes:
        field: 错误字段（可选）
        message: 错误消息
    """
    field: Optional[str] = None
    message: str
