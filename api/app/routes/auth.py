# 用户认证相关路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.schemas.base import ApiResponse
from app.schemas.user import WxLoginRequest, UserResponse
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()


@router.post("/login", response_model=ApiResponse[UserResponse])
async def wx_login(
    login_data: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """
    微信登录
    
    接收微信code,调用微信API获取openid,创建或更新用户记录
    
    - **code**: 微信登录凭证
    - **nick_name**: 用户昵称(可选)
    - **avatar_url**: 用户头像URL(可选)
    """
    # 调用微信API获取openid
    wx_data = await UserService.wx_code_to_session(login_data.code)
    open_id = wx_data.get("openid")
    
    if not open_id:
        raise HTTPException(status_code=400, detail="获取openid失败")
    
    # 查询用户是否存在
    user = UserService.get_user_by_openid(db, open_id)
    
    if user:
        # 用户已存在,更新信息
        update_data = UserUpdate(
            nick_name=login_data.nick_name,
            avatar_url=login_data.avatar_url
        )
        user = UserService.update_user(db, user, update_data)
    else:
        # 创建新用户
        create_data = UserCreate(
            open_id=open_id,
            nick_name=login_data.nick_name,
            avatar_url=login_data.avatar_url
        )
        user = UserService.create_user(db, create_data)
    
    return ApiResponse(
        code=200,
        message="登录成功",
        data=UserResponse.model_validate(user)
    )


@router.get("/user", response_model=ApiResponse[UserResponse])
def get_user_info(
    open_id: str,
    db: Session = Depends(get_db)
):
    """
    获取用户信息
    
    根据openid获取用户详细信息
    
    - **open_id**: 微信OpenID
    """
    user = UserService.get_user_by_openid(db, open_id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"用户不存在 (OpenID: {open_id})")
    
    return ApiResponse(
        code=200,
        message="获取用户信息成功",
        data=UserResponse.model_validate(user)
    )


@router.put("/user/nickname", response_model=ApiResponse[UserResponse])
def update_nickname(
    open_id: str,
    nick_name: str,
    db: Session = Depends(get_db)
):
    """
    修改用户昵称
    
    - **open_id**: 微信OpenID
    - **nick_name**: 新昵称
    """
    # 验证昵称
    if not nick_name or nick_name.strip() == "":
        raise HTTPException(status_code=400, detail="昵称不能为空")
    
    if len(nick_name) > 20:
        raise HTTPException(status_code=400, detail="昵称长度不能超过20个字符")
    
    # 获取用户
    user = UserService.get_user_by_openid(db, open_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新昵称
    update_data = UserUpdate(nick_name=nick_name.strip())
    user = UserService.update_user(db, user, update_data)
    
    return ApiResponse(
        code=200,
        message="昵称修改成功",
        data=UserResponse.model_validate(user)
    )
