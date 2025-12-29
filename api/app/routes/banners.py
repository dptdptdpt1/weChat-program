# 顶部滚动栏相关路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.database import get_db
from app.models.banner import Banner

router = APIRouter()


@router.get("")
async def get_banners(
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """
    获取顶部滚动栏列表
    
    - **is_active**: 是否只获取启用的轮播图（默认 true）
    """
    try:
        query = db.query(Banner)
        
        # 筛选启用状态
        if is_active:
            query = query.filter(Banner.is_active == True)
        
        # 按排序顺序排序
        banners = query.order_by(Banner.sort_order.asc(), Banner.id.asc()).all()
        
        # 转换为字典列表
        banner_list = [
            {
                "id": banner.id,
                "image_url": banner.image_url,
                "title": banner.title,
                "link_url": banner.link_url,
                "sort_order": banner.sort_order,
                "is_active": banner.is_active,
                "created_at": banner.created_at.isoformat() if banner.created_at else None,
                "updated_at": banner.updated_at.isoformat() if banner.updated_at else None
            }
            for banner in banners
        ]
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": banner_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取轮播图失败: {str(e)}")
