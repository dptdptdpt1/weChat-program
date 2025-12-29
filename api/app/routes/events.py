# 赛事相关路由
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.utils.database import get_db
from app.schemas.base import ApiResponse, PaginatedResponse
from app.schemas.event import EventResponse, EventCreate, EventUpdate
from app.services.event_service import EventService

router = APIRouter()


@router.get("", response_model=ApiResponse[PaginatedResponse[EventResponse]])
def get_events(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    keyword: Optional[str] = Query(None, max_length=100, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取赛事列表
    
    支持分页和关键词搜索
    
    - **page**: 页码,从1开始
    - **page_size**: 每页大小,最大100
    - **keyword**: 搜索关键词,匹配赛事标题
    """
    # 获取赛事列表
    events, total = EventService.get_events(
        db=db,
        page=page,
        page_size=page_size,
        keyword=keyword
    )
    
    # 构建分页响应
    has_more = (page * page_size) < total
    
    paginated_data = PaginatedResponse(
        items=[EventResponse.model_validate(event) for event in events],
        total=total,
        page=page,
        page_size=page_size,
        has_more=has_more
    )
    
    return ApiResponse(
        code=200,
        message="获取赛事列表成功",
        data=paginated_data
    )


@router.get("/{event_id}", response_model=ApiResponse[EventResponse])
def get_event_detail(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    获取赛事详情
    
    - **event_id**: 赛事ID
    """
    event = EventService.get_event_by_id(db, event_id)
    
    return ApiResponse(
        code=200,
        message="获取赛事详情成功",
        data=EventResponse.model_validate(event)
    )


@router.post("/{event_id}/view", response_model=ApiResponse[EventResponse])
def increase_view_count(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    增加赛事浏览量
    
    - **event_id**: 赛事ID
    """
    event = EventService.increase_view_count(db, event_id)
    
    return ApiResponse(
        code=200,
        message="浏览量增加成功",
        data=EventResponse.model_validate(event)
    )


@router.post("", response_model=ApiResponse[EventResponse])
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):
    """
    创建赛事 (管理员功能)
    
    - **event_data**: 赛事数据
    """
    event = EventService.create_event(db, event_data)
    
    return ApiResponse(
        code=200,
        message="创建赛事成功",
        data=EventResponse.model_validate(event)
    )


@router.put("/{event_id}", response_model=ApiResponse[EventResponse])
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db)
):
    """
    更新赛事 (管理员功能)
    
    - **event_id**: 赛事ID
    - **event_data**: 更新数据
    """
    event = EventService.update_event(db, event_id, event_data)
    
    return ApiResponse(
        code=200,
        message="更新赛事成功",
        data=EventResponse.model_validate(event)
    )


@router.delete("/{event_id}", response_model=ApiResponse[None])
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    删除赛事 (管理员功能)
    
    - **event_id**: 赛事ID
    """
    EventService.delete_event(db, event_id)
    
    return ApiResponse(
        code=200,
        message="删除赛事成功",
        data=None
    )
