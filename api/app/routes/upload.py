# 文件上传相关路由
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime
from pathlib import Path

from app.utils.database import get_db
from app.models.uploaded_image import UploadedImage

router = APIRouter()

# 上传目录配置
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def ensure_upload_dir():
    """确保上传目录存在"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    (UPLOAD_DIR / "events").mkdir(exist_ok=True)
    (UPLOAD_DIR / "thumbnails").mkdir(exist_ok=True)
    (UPLOAD_DIR / "banners").mkdir(exist_ok=True)


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()


def generate_filename(original_filename: str) -> str:
    """生成唯一文件名"""
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    type: str = "event",  # event, thumbnail, 或 banner
    db: Session = Depends(get_db)
):
    """
    上传图片
    
    - **file**: 图片文件
    - **type**: 图片类型 (event: 赛事图片, thumbnail: 缩略图, banner: 轮播图)
    
    返回图片访问URL和Markdown语法
    """
    # 验证文件扩展名
    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。允许的格式: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 读取文件内容
    contents = await file.read()
    
    # 验证文件大小
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件太大。最大允许 {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 确保上传目录存在
    ensure_upload_dir()
    
    # 生成文件名
    filename = generate_filename(file.filename)
    
    # 确定保存路径
    if type == "thumbnail":
        save_dir = UPLOAD_DIR / "thumbnails"
    elif type == "banner":
        save_dir = UPLOAD_DIR / "banners"
    else:
        save_dir = UPLOAD_DIR / "events"
    
    file_path = save_dir / filename
    
    # 保存文件
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"保存文件失败: {str(e)}"
        )
    
    # 返回访问URL
    url = f"/uploads/{type}s/{filename}"
    
    # 保存到数据库
    uploaded_image = UploadedImage(
        filename=filename,
        url=url,
        size=len(contents),
        type=type,
        created_at=datetime.utcnow()
    )
    db.add(uploaded_image)
    db.commit()
    db.refresh(uploaded_image)
    
    return {
        "code": 200,
        "message": "上传成功",
        "data": {
            "id": uploaded_image.id,
            "url": url,
            "filename": filename,
            "size": len(contents),
            "type": type,
            "markdown": f"![图片描述]({url})",
            "html": f'<img src="{url}" alt="图片" />'
        }
    }


@router.delete("/image")
async def delete_image(url: str):
    """
    删除图片
    
    - **url**: 图片URL
    """
    # 从URL提取文件路径
    if not url.startswith("/uploads/"):
        raise HTTPException(status_code=400, detail="无效的图片URL")
    
    # 构建文件路径
    file_path = Path(url[1:])  # 移除开头的 /
    
    # 检查文件是否存在
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 删除文件
    try:
        file_path.unlink()
        return {
            "code": 200,
            "message": "删除成功",
            "data": {"url": url}
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除文件失败: {str(e)}"
        )
