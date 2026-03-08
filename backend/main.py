"""
AI买手助手 - 完整版后端API v2
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="AI Fashion Buyer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据模型 ====================

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str = "buyer"

class Product(BaseModel):
    id: int
    name: str
    category: str
    brand: str
    price: float
    sales_count: int = 0

class Supplier(BaseModel):
    id: int
    name: str
    quality_score: float
    price_score: float
    delivery_score: float
    moq: int

class Trend(BaseModel):
    id: int
    title: str
    source: str
    trend_score: float
    tags: List[str] = []

# ==================== 数据库 ====================

products = [
    {"id": 1, "name": "简约白色T恤", "category": "T恤", "brand": "优衣库", "price": 89, "sales_count": 1520},
    {"id": 2, "name": "复古牛仔裤", "category": "裤子", "brand": "Levi's", "price": 299, "sales_count": 890},
    {"id": 3, "name": "职场西装外套", "category": "外套", "brand": "GXG", "price": 599, "sales_count": 456},
    {"id": 4, "name": "春季连衣裙", "category": "裙子", "brand": "ZARA", "price": 399, "sales_count": 1230},
    {"id": 5, "name": "运动休闲鞋", "category": "鞋子", "brand": "Nike", "price": 459, "sales_count": 2100},
    {"id": 6, "name": "羊毛大衣", "category": "外套", "brand": "MaxMara", "price": 1299, "sales_count": 120},
    {"id": 7, "name": "条纹衬衫", "category": "衬衫", "brand": "海澜之家", "price": 159, "sales_count": 780},
    {"id": 8, "name": "半身裙", "category": "裙子", "brand": "UR", "price": 269, "sales_count": 560},
]

suppliers = [
    {"id": 1, "name": "杭州丝绸厂", "quality_score": 9.2, "price_score": 8.5, "delivery_score": 9.0, "moq": 100},
    {"id": 2, "name": "广州服装代工厂", "quality_score": 8.8, "price_score": 9.5, "delivery_score": 8.8, "moq": 50},
    {"id": 3, "name": "苏州纺织集团", "quality_score": 9.5, "price_score": 8.0, "delivery_score": 9.2, "moq": 200},
    {"id": 4, "name": "东莞运动用品厂", "quality_score": 9.0, "price_score": 9.0, "delivery_score": 9.5, "moq": 200},
]

trends = [
    {"id": 1, "title": "春季职场穿搭", "source": "小红书", "trend_score": 9.2, "tags": ["职场", "春季"]},
    {"id": 2, "title": "复古风回潮", "source": "微博", "trend_score": 8.8, "tags": ["复古", "潮流"]},
    {"id": 3, "title": "运动休闲风格", "source": "抖音", "trend_score": 9.5, "tags": ["运动", "休闲"]},
    {"id": 4, "title": "新中式穿搭", "source": "小红书", "trend_score": 9.0, "tags": ["新中式", "国风"]},
    {"id": 5, "title": "多巴胺配色", "source": "微博", "trend_score": 8.5, "tags": ["多巴胺", "亮色"]},
]

# ==================== API路由 ====================

@app.get("/")
def root():
    return {"name": "AI Fashion Buyer API", "version": "2.0.0", "status": "running", "time": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/products", response_model=List[Product])
def get_products(category: Optional[str] = None, limit: int = 20):
    if category:
        return [p for p in products if p["category"] == category][:limit]
    return products[:limit]

@app.get("/api/v1/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="商品不存在")

@app.get("/api/v1/suppliers", response_model=List[Supplier])
def get_suppliers(limit: int = 20):
    return suppliers[:limit]

@app.get("/api/v1/suppliers/{supplier_id}")
def get_supplier(supplier_id: int):
    for s in suppliers:
        if s["id"] == supplier_id:
            return s
    raise HTTPException(status_code=404, detail="供应商不存在")

@app.get("/api/v1/recommendations")
def get_recommendations(limit: int = 10):
    sorted_products = sorted(products, key=lambda x: x["sales_count"], reverse=True)
    return [{"product": p, "score": 1.0 - i*0.1, "reason": "热门推荐"} for i, p in enumerate(sorted_products[:limit])]

@app.get("/api/v1/trends", response_model=List[Trend])
def get_trends(limit: int = 20):
    return trends[:limit]

@app.get("/api/v1/trends/analysis")
def get_trend_analysis():
    return {
        "total": len(trends),
        "avg_score": sum(t["trend_score"] for t in trends) / len(trends),
        "by_source": [{"source": t["source"], "count": sum(1 for x in trends if x["source"] == t["source"])} for t in set((x["source"], x) for x in trends)]
    }

@app.get("/api/v1/stats/summary")
def get_stats():
    return {
        "total_products": len(products),
        "total_suppliers": len(suppliers),
        "total_trends": len(trends),
        "categories": list(set(p["category"] for p in products)),
        "top_products": sorted(products, key=lambda x: x["sales_count"], reverse=True)[:5]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
