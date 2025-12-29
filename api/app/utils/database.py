# 数据库连接配置
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库 URL 配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./football_events.db")

# 创建数据库引擎
# SQLite 需要 check_same_thread=False 以支持多线程
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False  # 关闭 SQL 日志输出,减少日志噪音
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


# 数据库依赖注入函数
def get_db():
    """
    获取数据库会话
    用于 FastAPI 依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 初始化数据库表
def init_db():
    """
    创建所有数据库表
    在应用启动时调用
    """
    Base.metadata.create_all(bind=engine)
