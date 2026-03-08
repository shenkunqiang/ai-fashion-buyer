"""
AI买手助手 - 完整版后端API
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
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

# ==================== 数据模型 ====================

# 用户模型
class User(BaseModel):
    id: int
    username: str
    email: str
    role: str = "buyer"
    created_at: str

# 用户注册
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# 登录
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 商品
class Product(BaseModel):
    id: int
    name: str
    category: str
    sub_category: Optional[str] = None
    brand: str
    price: float
    cost_price: Optional[float] = None
    images: List[str] = []
    style_tags: List[str] = []
    color_tags: List[str] = []
    stock: int = 0
    sales_count: int = 0

# 供应商
class Supplier(BaseModel):
    id: int
    name: str
    company_name: Optional[str] = None
    contact: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    quality_score: float = 5.0
    price_score: float = 5.0
    delivery_score: float = 5.0
    moq: int = 1
    lead_time_days: int = 7
    is_verified: bool = False

# 趋势
class Trend(BaseModel):
    id: int
    title: str
    source: str
    content: Optional[str] = None
    media_urls: List[str] = []
    likes: int = 0
    comments: int = 0
    shares: int = 0
    tags: List[str] = []
    category: Optional[str] = None
    trend_score: float = 0.0

# 推荐
class Recommendation(BaseModel):
    product_id: int
    product: Product
    score: float
    reason: str

# 风格画像
class StyleProfile(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    style_type: Optional[str] = None
    feature_vector: dict = {}
    total_likes: int = 0

# ==================== 模拟数据库 ====================

users_db = []
products_db = [
    {"id": 1, "name": "简约白色T恤", "category": "T恤", "sub_category": "圆领", "brand": "优衣库", "price": 89, "cost_price": 45, "images": [], "style_tags": ["简约", "基础"], "color_tags": ["白色"], "stock": 1000, "sales_count": 1520},
    {"id": 2, "name": "复古牛仔裤", "category": "裤子", "sub_category": "直筒", "brand": "Levi's", "price": 299, "cost_price": 150, "images": [], "style_tags": ["复古", "潮流"], "color_tags": ["蓝色"], "stock": 500, "sales_count": 890},
    {"id": 3, "name": "职场西装外套", "category": "外套", "sub_category": "西装", "brand": "GXG", "price": 599, "cost_price": 300, "images": [], "style_tags": ["职场", "正式"], "color_tags": ["黑色", "灰色"], "stock": 200, "sales_count": 456},
    {"id": 4, "name": "春季连衣裙", "category": "裙子", "sub_category": "长裙", "brand": "ZARA", "price": 399, "cost_price": 180, "images": [], "style_tags": ["春季", "甜美"], "color_tags": ["粉色", "白色"], "stock": 300, "sales_count": 1230},
    {"id": 5, "name": "运动休闲鞋", "category": "鞋子", "sub_category": "运动鞋", "brand": "Nike", "price": 459, "cost_price": 220, "images": [], "style_tags": ["运动", "休闲"], "color_tags": ["白色", "黑色"], "stock": 800, "sales_count": 2100},
    {"id": 6, "name": "羊毛大衣", "category": "外套", "sub_category": "大衣", "brand": "MaxMara", "price": 1299, "cost_price": 600, "images": [], "style_tags": ["高端", "优雅"], "color_tags": ["驼色", "黑色"], "stock": 50, "sales_count": 120},
    {"id": 7, "name": "条纹衬衫", "category": "衬衫", "sub_category": "商务", "brand": "海澜之家", "price": 159, "cost_price": 70, "images": [], "style_tags": ["商务", "条纹"], "color_tags": ["蓝色", "白色"], "stock": 600, "sales_count": 780},
    {"id": 8, "name": "半身裙", "category": "裙子", "sub_category": "A字裙", "brand": "UR", "price": 269, "cost_price": 120, "images": [], "style_tags": ["A字", "显瘦"], "color_tags": ["黑色", "卡其"], "stock": 400, "sales_count": 560},
]

suppliers_db = [
    {"id": 1, "name": "杭州丝绸厂", "company_name": "杭州丝绸集团有限公司", "contact": "张经理", "phone": "13800001111", "email": "hangzhou@silk.com", "quality_score": 9.2, "price_score": 8.5, "delivery_score": 9.0, "moq": 100, "lead_time_days": 15, "is_verified": True},
    {"id": 2, "name": "广州服装代工厂", "company_name": "广州制衣厂", "contact": "李总", "phone": "13800002222", "email": "guangzhou@factory.com", "quality_score": 8.8, "price_score": 9.5, "delivery_score": 8.8, "moq": 50, "lead_time_days": 10, "is_verified": True},
    {"id": 3, "name": "苏州纺织集团", "company_name": "苏州纺织股份有限公司", "contact": "王主任", "phone": "13800003333", "email": "suzhou@textile.com", "quality_score": 9.5, "price_score": 8.0, "delivery_score": 9.2, "moq": 200, "lead_time_days": 20, "is_verified": True},
    {"id": 4, "name": "东莞运动用品厂", "company_name": "东莞运动用品有限公司", "contact": "刘生", "phone": "13800004444", "email": "dongguan@sports.com", "quality_score": 9.0, "price_score": 9.0, "delivery_score": 9.5, "moq": 200, "lead_time_days": 12, "is_verified": True},
]

trends_db = [
    {"id": 1, "title": "春季职场穿搭", "source": "小红书", "content": "春季职场穿搭指南...", "media_urls": [], "likes": 12500, "comments": 890, "shares": 456, "tags": ["职场", "春季", "穿搭"], "category": "穿搭", "trend_score": 9.2},
    {"id": 2, "title": "复古风回潮", "source": "微博", "content": "复古元素再次流行...", "media_urls": [], "likes": 8900, "comments": 567, "shares": 321, "tags": ["复古", "潮流", "回潮"], "category": "风格", "trend_score": 8.8},
    {"id": 3, "title": "运动休闲风格", "source": "抖音", "content": "运动休闲成主流...", "media_urls": [], "likes": 25600, "comments": 1230, "shares": 890, "tags": ["运动", "休闲", "舒适"], "category": "风格", "trend_score": 9.5},
    {"id": 4, "title": "新中式穿搭", "source": "小红书", "content": "传统与现代结合...", "media_urls": [], "likes": 15600, "comments": 780, "shares": 567, "tags": ["新中式", "传统", "国风"], "category": "风格", "trend_score": 9.0},
    {"id": 5, "title": "多巴胺配色", "source": "微博", "content": "高饱和度配色成趋势...", "media_urls": [], "likes": 11200, "comments": 650, "shares": 432, "tags": ["多巴胺", "配色", "亮色"], "category": "色彩", "trend_score": 8.5},
]

style_profiles_db = []

# ==================== API路由 ====================

@app.get("/")
def root():
    return {
        "name": "AI Fashion Buyer API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 用户
@app.post("/api/v1/users/register", response_model=User)
def register_user(user: UserCreate):
    new_id = len(users_db) + 1
    new_user = {
        "id": new_id,
        "username": user.username,
        "email": user.email,
        "role": "buyer",
        "created_at": datetime.now().isoformat()
    }
    users_db.append(new_user)
    return new_user

@app.post("/api/v1/users/login")
def login(credentials: LoginRequest):
    for u in users_db:
        if u["email"] == credentials.email:
            return {"access_token": f"token_{u['id']}", "user": u}
    # 模拟登录成功
    return {"access_token": "token_demo", "user": {"id": 1, "username": "demo", "email": credentials.email}}

# 商品
@app.get("/api/v1/products", response_model=List[Product])
def get_products(
    category: Optional[str] = None,
    style_tags: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = 1,
    page_size: int = 20
):
    results = products_db.copy()
    if category:
        results = [p for p in results if p["category"] == category]
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]
    start = (page - 1) * page_size
    return results[start:start + page_size]

@app.get("/api/v1/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in products_db:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="商品不存在")

@app.get("/api/v1/products/categories")
def get_categories():
    categories = list(set(p["category"] for p in products_db))
    return {"categories": categories}

# 供应商
@app.get("/api/v1/suppliers", response_model=List[Supplier])
def get_suppliers(
    category: Optional[str] = None,
    min_score: Optional[float] = None,
    page: int = 1,
    page_size: int = 20
):
    results = suppliers_db.copy()
    if min_score is not None:
        results = [s for s in results if s["quality_score"] >= min_score]
    start = (page - 1) * page_size
    return results[start:start + page_size]

@app.get("/api/v1/suppliers/{supplier_id}", response_model=Supplier)
def get_supplier(supplier_id: int):
    for s in suppliers_db:
        if s["id"] == supplier_id:
            return s
    raise HTTPException(status_code=404, detail="供应商不存在")

@app.get("/api/v1/suppliers/{supplier_id}/match/{product_id}")
def calculate_match(supplier_id: int, product_id: int):
    """计算供应商与商品的匹配度"""
    supplier = next((s for s in suppliers_db if s["id"] == supplier_id), None)
    product = next((p for p in products_db if p["id"] == product_id), None)
    
    if not supplier or not product:
        raise HTTPException(status_code=404, detail="供应商或商品不存在")
    
    # 简化匹配算法
    quality_match = supplier["quality_score"] / 10 * 100
    price_match = supplier["price_score"] / 10 * 100
    delivery_match = supplier["delivery_score"] / 10 * 100
    overall = (quality_match * 0.4 + price_match * 0.3 + delivery_match * 0.3)
    
    reasons = []
    if quality_match > 85:
        reasons.append("质量评分优秀")
    if price_match > 85:
        reasons.append("价格有竞争力")
    if delivery_match > 85:
        reasons.append("交货及时")
    
    return {
        "supplier_id": supplier_id,
        "product_id": product_id,
        "overall_match": round(overall, 1),
        "quality_match": quality_match,
        "price_match": price_match,
        "delivery_match": delivery_match,
        "reasons": reasons
    }

# 推荐
@app.get("/api/v1/recommendations", response_model=List[Recommendation])
def get_recommendations(user_id: Optional[int] = None, limit: int = 10, recommendation_type: str = "personalized"):
    """获取推荐列表"""
    results = []
    for i, p in enumerate(products_db[:limit]):
        score = 0.95 - i * 0.08
        reason = "热门推荐" if recommendation_type == "trending" else "根据您的偏好推荐"
        results.append({
            "product_id": p["id"],
            "product": p,
            "score": round(score, 2),
            "reason": reason
        })
    return results

# 趋势
@app.get("/api/v1/trends", response_model=List[Trend])
def get_trends(
    category: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 20
):
    results = trends_db.copy()
    if category:
        results = [t for t in results if t.get("category") == category]
    if source:
        results = [t for t in results if t["source"] == source]
    return results[:limit]

@app.get("/api/v1/trends/analysis")
def get_trend_analysis(category: Optional[str] = None):
    """获取趋势分析"""
    results = trends_db.copy()
    if category:
        results = [t for t in results if t.get("category") == category]
    
    if not results:
        return {"category": category, "total_trends": 0, "avg_score": 0}
    
    avg_score = sum(t["trend_score"] for t in results) / len(results)
    
    # 统计标签
    tag_counts = {}
    for t in results:
        for tag in t.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "category": category,
        "total_trends": len(results),
        "avg_score": round(avg_score, 2),
        "top_tags": [{"tag": t[0], "count": t[1]} for t in top_tags],
        "trends_by_source": [{"source": t["source"], "count": sum(1 for x in results if x["source"] == t["source"])} for t in set(t["source"] for t in results)]
    }

# 风格画像
@app.post("/api/v1/styles/profiles", response_model=StyleProfile)
def create_style_profile(profile: dict):
    new_id = len(style_profiles_db) + 1
    new_profile = {
        "id": new_id,
        "user_id": profile.get("user_id", 1),
        "name": profile.get("name"),
        "description": profile.get("description"),
        "style_type": profile.get("style_type"),
        "feature_vector": {},
        "total_likes": 0
    }
    style_profiles_db.append(new_profile)
    return new_profile

@app.get("/api/v1/styles/profiles", response_model=List[StyleProfile])
def get_style_profiles(user_id: Optional[int] = None):
    if user_id:
        return [p for p in style_profiles_db if p["user_id"] == user_id]
    return style_profiles_db

# 统计
@app.get("/api/v1/stats/summary")
def get_stats():
    """获取系统统计"""
    return {
        "total_products": len(products_db),
        "total_suppliers": len(suppliers_db),
        "total_trends": len(trends_db),
        "total_users": len(users_db),
        "categories": list(set(p["category"] for p in products_db)),
        "top_products": sorted(products_db, key=lambda x: x["sales_count"], reverse=True)[:5]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
