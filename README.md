# 🛍️ AI Fashion Buyer - 衣舞台AI买手助手

基于"买手数字孪生 + 流行趋势预测"双引擎的智能服装采购平台。

## 🏗️ 技术架构

### 后端
- **FastAPI** - 高性能Python Web框架
- **PostgreSQL** - 主数据库
- **Redis** - 缓存层
- **SQLAlchemy** - ORM

### 前端
- **React 18** - UI框架
- **Ant Design** - 企业级UI组件库
- **TypeScript** - 类型安全
- **Next.js** - SSR框架

### AI/ML
- **推荐系统** - 个性化推荐 + 协同过滤
- **风格建模** - LoRA微调
- **趋势分析** - 多源数据聚合

## 📦 快速部署

### 使用Docker Compose

```bash
docker-compose up -d
```

### 访问

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- 前端: http://localhost:3000
- Nginx: http://localhost:80

## 📱 功能模块

1. 👤 用户系统 - 注册、登录、权限管理
2. 🎨 风格画像 - 买手数字孪生
3. 📊 智能推荐 - 个性化商品推荐
4. 📈 趋势分析 - 流行趋势预测
5. 🏭 供应商管理 - 智能匹配
6. 📦 订单管理 - 采购流程

## 🔧 开发

### 本地开发
```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

## 📄 License
MIT
