"""
AI买手助手 - 管理后台API
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter(prefix="/api/v1/admin", tags=["管理"])

# 数据模型
class DashboardStats(BaseModel):
    total_products: int
    total_suppliers: int
    total_trends: int
    total_orders: int
    today_visits: int

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: str
    created_at: str

# 模拟数据库
orders_db = [
    {"id": 1, "user_id": 1, "product_id": 1, "quantity": 100, "status": "pending", "created_at": "2026-03-09T10:00:00"},
    {"id": 2, "user_id": 1, "product_id": 3, "quantity": 50, "status": "confirmed", "created_at": "2026-03-09T11:00:00"},
    {"id": 3, "user_id": 2, "product_id": 5, "quantity": 200, "status": "shipped", "created_at": "2026-03-08T15:00:00"},
]

# 路由
@router.get("/dashboard")
def get_dashboard():
    """获取仪表盘统计"""
    return {
        "total_products": 8,
        "total_suppliers": 4,
        "total_trends": 5,
        "total_orders": len(orders_db),
        "today_visits": random.randint(100, 500)
    }

@router.get("/orders", response_model=List[Order])
def get_orders(status: Optional[str] = None):
    """获取订单列表"""
    if status:
        return [o for o in orders_db if o["status"] == status]
    return orders_db

@router.post("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str):
    """更新订单状态"""
    for o in orders_db:
        if o["id"] == order_id:
            o["status"] = status
            return {"success": True, "order": o}
    raise HTTPException(status_code=404, detail="订单不存在")

# 简单的random函数
import random
