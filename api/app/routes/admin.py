# 后台管理相关路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.schemas.base import ApiResponse
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.models.event import Event
from app.utils.markdown_helper import extract_first_image
from datetime import datetime

router = APIRouter()


@router.post("/events", response_model=ApiResponse[EventResponse])
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):
    """
    创建赛事
    
    - **title**: 赛事标题
    - **date**: 赛事日期
    - **content**: 赛事内容(Markdown格式)
    """
    # 从 Markdown 内容中提取封面图
    cover_image = extract_first_image(event_data.content) if event_data.content else None
    
    # 创建赛事
    event = Event(
        title=event_data.title,
        date=event_data.date,
        content=event_data.content,
        cover_image=cover_image,
        view_count=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return ApiResponse(
        code=200,
        message="赛事创建成功",
        data=EventResponse.model_validate(event)
    )


@router.put("/events/{event_id}", response_model=ApiResponse[EventResponse])
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db)
):
    """
    更新赛事
    
    - **event_id**: 赛事ID
    - **title**: 赛事标题(可选)
    - **date**: 赛事日期(可选)
    - **content**: 赛事内容(可选)
    """
    # 查询赛事
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail=f"赛事不存在 (ID: {event_id})")
    
    # 更新字段
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    # 如果内容更新了，重新提取封面图
    if 'content' in update_data and update_data['content']:
        event.cover_image = extract_first_image(update_data['content'])
    
    event.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(event)
    
    return ApiResponse(
        code=200,
        message="赛事更新成功",
        data=EventResponse.model_validate(event)
    )


@router.delete("/events/{event_id}", response_model=ApiResponse[dict])
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    删除赛事
    
    - **event_id**: 赛事ID
    """
    # 查询赛事
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail=f"赛事不存在 (ID: {event_id})")
    
    # 删除赛事
    db.delete(event)
    db.commit()
    
    return ApiResponse(
        code=200,
        message="赛事删除成功",
        data={"id": event_id}
    )
