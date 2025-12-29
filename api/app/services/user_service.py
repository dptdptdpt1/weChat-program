# 用户服务层
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import httpx
import os
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """用户服务类"""
    
    # 微信API配置 (从环境变量读取)
    WX_APP_ID = os.getenv("WECHAT_APP_ID", "")
    WX_APP_SECRET = os.getenv("WECHAT_APP_SECRET", "")
    WX_API_URL = "https://api.weixin.qq.com/sns/jscode2session"
    
    @staticmethod
    async def wx_code_to_session(code: str) -> dict:
        """
        调用微信API,通过code换取openid和session_key
        
        Args:
            code: 微信登录凭证
            
        Returns:
            包含openid和session_key的字典
            
        Raises:
            HTTPException: 当微信API调用失败时
        """
        params = {
            "appid": UserService.WX_APP_ID,
            "secret": UserService.WX_APP_SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(UserService.WX_API_URL, params=params)
                data = response.json()
                
                # 检查是否有错误
                if "errcode" in data and data["errcode"] != 0:
                    raise HTTPException(
                        status_code=400,
                        detail=f"微信登录失败: {data.get('errmsg', '未知错误')}"
                    )
                
                return data
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"调用微信API失败: {str(e)}"
            )
    
    @staticmethod
    def get_user_by_openid(db: Session, open_id: str) -> Optional[User]:
        """
        根据openid获取用户
        
        Args:
            db: 数据库会话
            open_id: 微信OpenID
            
        Returns:
            用户对象,如果不存在则返回None
        """
        return db.query(User).filter(User.open_id == open_id).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        创建新用户
        
        Args:
            db: 数据库会话
            user_data: 用户创建数据
            
        Returns:
            创建的用户对象
        """
        # 如果没有提供昵称，生成随机昵称
        nick_name = user_data.nick_name
        if not nick_name or nick_name.strip() == "":
            nick_name = UserService._generate_random_nickname()
        
        user = User(
            open_id=user_data.open_id,
            nick_name=nick_name,
            avatar_url=user_data.avatar_url,
            created_at=datetime.utcnow(),
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def _generate_random_nickname() -> str:
        """
        生成随机昵称
        
        Returns:
            随机昵称字符串
        """
        import random
        
        # 昵称前缀列表
        prefixes = [
            "足球迷", "球迷", "赛事通", "足球fans", "球场",
            "绿茵", "射手", "守门员", "中场", "后卫",
            "前锋", "教练", "裁判", "观众", "球评"
        ]
        
        # 生成4位随机数字
        random_num = random.randint(1000, 9999)
        
        # 随机选择一个前缀
        prefix = random.choice(prefixes)
        
        return f"{prefix}{random_num}"
    
    @staticmethod
    def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
        """
        更新用户信息
        
        Args:
            db: 数据库会话
            user: 用户对象
            user_data: 更新数据
            
        Returns:
            更新后的用户对象
        """
        if user_data.nick_name is not None:
            user.nick_name = user_data.nick_name
        if user_data.avatar_url is not None:
            user.avatar_url = user_data.avatar_url
        
        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_last_login(db: Session, user: User) -> User:
        """
        更新用户最后登录时间
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            更新后的用户对象
        """
        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
