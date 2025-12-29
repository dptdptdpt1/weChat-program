from fastapi import APIRouter
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/health", response_model=ApiResponse[dict])
def health_check():
    """
    健康检查接口
    
    Returns:
        ApiResponse: 包含服务状态的响应
    """
    return ApiResponse(
        code=200,
        message="服务运行正常",
        data={
            "status": "ok",
            "service": "宝利足球赛事通 API"
        }
    )
