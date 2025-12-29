# 配置相关路由
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.schemas.base import ApiResponse
from app.schemas.customer_service import CustomerServiceResponse
from app.services.customer_service import CustomerServiceService

router = APIRouter()


@router.get("/customer-service", response_model=ApiResponse[CustomerServiceResponse])
def get_customer_service_config(db: Session = Depends(get_db)):
    """
    获取客服配置
    
    返回客服二维码URL和在线时间
    """
    config = CustomerServiceService.get_config(db)
    
    return ApiResponse(
        code=200,
        message="获取客服配置成功",
        data=CustomerServiceResponse.model_validate(config)
    )
