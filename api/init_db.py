#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本

创建所有数据库表并填充初始数据
"""

import sys
import os
from datetime import date, datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.database import engine, SessionLocal, Base
from app.models import Event, User, CustomerService, Banner


def create_tables():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建成功")


def init_customer_service(db):
    """初始化客服配置"""
    print("\n正在初始化客服配置...")
    
    # 检查是否已存在配置
    existing = db.query(CustomerService).first()
    if existing:
        # 更新现有配置的图片路径（如果还是旧路径）
        if existing.qr_code_url == "/assets/images/customer-service-qr.jpg":
            existing.qr_code_url = "/uploads/customer-service/customer-service-qr.jpg"
            db.commit()
            print("✓ 客服配置已更新为后端路径")
        else:
            print("✓ 客服配置已存在,跳过初始化")
        return
    
    # 创建默认客服配置
    customer_service = CustomerService(
        # 客服二维码图片路径（后端存储）
        qr_code_url="/uploads/customer-service/customer-service-qr.jpg",
        online_time="工作日 9:00-18:00"  # 客服在线时间
    )
    
    db.add(customer_service)
    db.commit()
    print("✓ 客服配置初始化成功")


def init_sample_events(db):
    """初始化示例赛事数据"""
    print("\n正在初始化示例赛事数据...")
    
    # 检查是否已存在赛事
    existing_count = db.query(Event).count()
    if existing_count > 0:
        print(f"✓ 已存在 {existing_count} 条赛事数据,跳过初始化")
        return
    
    # 不创建示例赛事，由管理员在后台手动添加
    print("✓ 跳过示例赛事创建，请在后台管理界面手动添加赛事")


def init_banners(db):
    """初始化轮播图数据"""
    print("\n正在初始化轮播图数据...")
    
    # 检查是否已存在轮播图
    existing_count = db.query(Banner).count()
    if existing_count > 0:
        print(f"✓ 已存在 {existing_count} 条轮播图数据,跳过初始化")
        return
    
    # 创建默认轮播图（6张）
    banners_data = [
        {
            "image_url": "/uploads/banners/54980db6df5d047f83d48a22de10cd9f.jpg",
            "title": "精彩赛事",
            "sort_order": 10,
            "is_active": True
        },
        {
            "image_url": "/uploads/banners/697a95e306df2c75238543ee5bf7f061.jpg",
            "title": "热门推荐",
            "sort_order": 20,
            "is_active": True
        },
        {
            "image_url": "/uploads/banners/9e79e83e3874de5a3a6a6c85f1365824.jpg",
            "title": "今日方案",
            "sort_order": 30,
            "is_active": True
        },
        {
            "image_url": "/uploads/banners/a4d45564a9b94f941fd33c1dc7db4358.jpg",
            "title": "专家推荐",
            "sort_order": 40,
            "is_active": True
        },
        {
            "image_url": "/uploads/banners/b110fd9b79c844651a4aa0ef70370006.jpg",
            "title": "赛事分析",
            "sort_order": 50,
            "is_active": True
        },
        {
            "image_url": "/uploads/banners/cc12009683308099fec3542ce7b64021.jpg",
            "title": "足球资讯",
            "sort_order": 60,
            "is_active": True
        }
    ]
    
    for banner_data in banners_data:
        banner = Banner(**banner_data)
        db.add(banner)
    
    db.commit()
    print(f"✓ 成功创建 {len(banners_data)} 条轮播图数据")


def main():
    """主函数"""
    print("=" * 60)
    print("数据库初始化")
    print("=" * 60)
    
    try:
        # 创建表
        create_tables()
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 初始化客服配置
            init_customer_service(db)
            
            # 初始化示例赛事
            init_sample_events(db)
            
            # 初始化轮播图
            init_banners(db)
            
            print("\n" + "=" * 60)
            print("✓ 数据库初始化完成!")
            print("=" * 60)
            
            # 显示统计信息
            event_count = db.query(Event).count()
            user_count = db.query(User).count()
            cs_count = db.query(CustomerService).count()
            banner_count = db.query(Banner).count()
            
            print(f"\n数据统计:")
            print(f"  赛事数量: {event_count}")
            print(f"  用户数量: {user_count}")
            print(f"  客服配置: {cs_count}")
            print(f"  轮播图: {banner_count}")
            
        finally:
            db.close()
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
