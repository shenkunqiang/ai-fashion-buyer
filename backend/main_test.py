"""
AI买手助手 - 简化版后端API（用于测试）
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="AI Fashion Buyer API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 测试数据
products_db = [
    {"id": 1, "name": "简约白色T恤", "category": "T恤", "price": 89, "brand": "优衣库", "sales_count": 1520},
    {"id": 2, "name": "复古牛仔裤", "category": "裤子", "price": 299, "brand": "Levi's", "sales_count": 890},
    {"id": 3, "name": "职场西装外套", "category": "外套", "price": 599, "brand": "GXG", "sales_count": 456},
    {"id": 4, "name": "春季连衣裙", "category": "裙子", "price": 399, "brand": "ZARA", "sales_count": 1230},
    {"id": 5, "name": "运动休闲鞋", "category": "鞋子", "price": 459, "brand": "Nike", "sales_count": 2100},
]

suppliers_db = [
    {"id": 1, "name": "杭州丝绸厂", "quality_score": 9.2, "price_score": 8.5, "delivery_score": 9.0, "moq": 100},
    {"id": 2, "name": "广州服装代工厂", "quality_score": 8.8, "price_score": 9.5, "delivery_score": 8.8, "moq": 50},
    {"id": 3, "name": "苏州纺织集团", "quality_score": 9.5, "price_score": 8.0, "delivery_score": 9.2, "moq": 200},
]

# 路由
@app.get("/")
def root():
    return {"name": "AI Fashion Buyer API", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/products")
def get_products(category: Optional[str] = None, limit: int = 20):
    if category:
        return [p for p in products_db if p["category"] == category][:limit]
    return products_db[:limit]

@app.get("/api/v1/products/{product_id}")
def get_product(product_id: int):
    for p in products_db:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="商品不存在")

@app.get("/api/v1/suppliers")
def get_suppliers(limit: int = 20):
    return suppliers_db[:limit]

@app.get("/api/v1/suppliers/{supplier_id}")
def get_supplier(supplier_id: int):
    for s in suppliers_db:
        if s["id"] == supplier_id:
            return s
    raise HTTPException(status_code=404, detail="供应商不存在")

@app.get("/api/v1/recommendations")
def get_recommendations(user_id: Optional[int] = None, limit: int = 10):
    """获取推荐列表"""
    return [
        {"product_id": p["id"], "product": p, "score": 0.95 - i*0.1, "reason": "热门推荐"}
        for i, p in enumerate(products_db[:limit])
    ]

@app.get("/api/v1/trends")
def get_trends(category: Optional[str] = None, limit: int = 20):
    """获取趋势数据"""
    return [
        {"id": 1, "title": "春季职场穿搭", "source": "小红书", "trend_score": 9.2, "tags": ["职场", "春季"]},
        {"id": 2, "title": "复古风回潮", "source": "微博", "trend_score": 8.8, "tags": ["复古", "潮流"]},
        {"id": 3, "title": "运动休闲风格", "source": "抖音", "trend_score": 9.5, "tags": ["运动", "休闲"]},
    ][:limit]

if __name__ == "__main__":
    print("🚀 启动AI买手助手后端服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
