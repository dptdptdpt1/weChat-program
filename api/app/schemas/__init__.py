# Pydantic 模式
from .base import ApiResponse, PaginatedResponse, ErrorDetail
from .event import EventBase, EventCreate, EventUpdate, EventResponse, EventListQuery
from .user import UserBase, UserCreate, UserUpdate, UserResponse, WxLoginRequest
from .customer_service import (
    CustomerServiceBase,
    CustomerServiceCreate,
    CustomerServiceUpdate,
    CustomerServiceResponse
)

__all__ = [
    "ApiResponse",
    "PaginatedResponse",
    "ErrorDetail",
    "EventBase",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "EventListQuery",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "WxLoginRequest",
    "CustomerServiceBase",
    "CustomerServiceCreate",
    "CustomerServiceUpdate",
    "CustomerServiceResponse",
]
