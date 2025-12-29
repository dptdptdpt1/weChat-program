# 赛事业务逻辑服务
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, Tuple, List
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.utils.exceptions import NotFoundException


class EventService:
    """赛事服务类"""
    
    @staticmethod
    def get_events(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None
    ) -> Tuple[List[Event], int]:
        """
        获取赛事列表(支持分页和搜索)
        
        Args:
            db: 数据库会话
            page: 页码
            page_size: 每页大小
            keyword: 搜索关键词
            
        Returns:
            (赛事列表, 总数量)
        """
        # 构建查询
        query = db.query(Event)
        
        # 搜索过滤
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(Event.title.like(search_pattern))
        
        # 按日期降序排序
        query = query.order_by(Event.date.desc())
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        events = query.offset(offset).limit(page_size).all()
        
        return events, total
    
    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Event:
        """
        根据ID获取赛事详情
        
        Args:
            db: 数据库会话
            event_id: 赛事ID
            
        Returns:
            赛事对象
            
        Raises:
            NotFoundException: 赛事不存在
        """
        event = db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise NotFoundException(f"赛事不存在 (ID: {event_id})")
        
        return event
    
    @staticmethod
    def create_event(db: Session, event_data: EventCreate) -> Event:
        """
        创建赛事
        
        Args:
            db: 数据库会话
            event_data: 赛事数据
            
        Returns:
            创建的赛事对象
        """
        event = Event(**event_data.model_dump())
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def update_event(db: Session, event_id: int, event_data: EventUpdate) -> Event:
        """
        更新赛事
        
        Args:
            db: 数据库会话
            event_id: 赛事ID
            event_data: 更新数据
            
        Returns:
            更新后的赛事对象
            
        Raises:
            NotFoundException: 赛事不存在
        """
        event = EventService.get_event_by_id(db, event_id)
        
        # 更新字段
        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def delete_event(db: Session, event_id: int) -> None:
        """
        删除赛事
        
        Args:
            db: 数据库会话
            event_id: 赛事ID
            
        Raises:
            NotFoundException: 赛事不存在
        """
        event = EventService.get_event_by_id(db, event_id)
        db.delete(event)
        db.commit()
    
    @staticmethod
    def increase_view_count(db: Session, event_id: int) -> Event:
        """
        增加赛事浏览量
        
        Args:
            db: 数据库会话
            event_id: 赛事ID
            
        Returns:
            更新后的赛事对象
            
        Raises:
            NotFoundException: 赛事不存在
        """
        event = EventService.get_event_by_id(db, event_id)
        event.view_count += 1
        db.commit()
        db.refresh(event)
        return event
