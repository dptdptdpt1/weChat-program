#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新客服配置脚本
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.database import SessionLocal
from app.models import CustomerService


def main():
    """更新客服二维码路径"""
    print("正在更新客服配置...")
    
    db = SessionLocal()
    try:
        # 获取客服配置
        cs = db.query(CustomerService).first()
        if cs:
            # 更新二维码路径
            cs.qr_code_url = "/assets/images/customer-service-qr.jpg"
            db.commit()
            print(f"✓ 客服配置更新成功")
            print(f"  二维码路径: {cs.qr_code_url}")
            print(f"  在线时间: {cs.online_time}")
        else:
            print("✗ 未找到客服配置")
            return 1
    except Exception as e:
        print(f"✗ 更新失败: {e}")
        return 1
    finally:
        db.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
