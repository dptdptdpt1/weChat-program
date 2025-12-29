from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
import os
from pathlib import Path

# 加载环境变量
load_dotenv()

from app.routes import health
from app.routes import events
from app.routes import auth
from app.routes import config
from app.routes import admin as admin_routes
from app.routes import upload
from app.routes import banners
from app.utils.database import init_db, engine
from app.admin import setup_admin
from app.utils.exceptions import BaseAPIException
from app.utils.error_handlers import (
    base_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    启动时初始化数据库，关闭时清理资源
    """
    # 启动时执行
    logger.info("正在初始化数据库...")
    init_db()
    logger.info("数据库初始化完成")
    
    # 确保上传目录存在
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    (upload_dir / "events").mkdir(exist_ok=True)
    (upload_dir / "thumbnails").mkdir(exist_ok=True)
    (upload_dir / "banners").mkdir(exist_ok=True)
    logger.info("上传目录初始化完成")
    
    yield
    # 关闭时执行
    logger.info("应用关闭")


# 创建 FastAPI 应用实例
app = FastAPI(
    title="宝利足球赛事通 API",
    description="宝利足球赛事通小程序后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 中间件配置 - 支持跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理器
app.add_exception_handler(BaseAPIException, base_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册路由
app.include_router(health.router, prefix="/api", tags=["健康检查"])
app.include_router(events.router, prefix="/api/events", tags=["赛事管理"])
app.include_router(auth.router, prefix="/api/auth", tags=["用户认证"])
app.include_router(config.router, prefix="/api/config", tags=["系统配置"])
app.include_router(admin_routes.router, prefix="/api/admin", tags=["后台管理"])
app.include_router(upload.router, prefix="/api/upload", tags=["文件上传"])
app.include_router(banners.router, prefix="/api/banners", tags=["顶部滚动栏"])

# 挂载静态文件目录（上传的图片）
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 设置后台管理界面
setup_admin(app, engine)


@app.get("/")
def read_root():
    """
    根路径欢迎信息
    """
    return {
        "code": 200,
        "message": "欢迎使用宝利足球赛事通 API",
        "data": {
            "version": "1.0.0",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
