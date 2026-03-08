"""
AI买手助手 - 后端API主程序
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import routes
from app.core.database import init_db, close_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 AI买手助手后端启动中...")
    await init_db()
    yield
    logger.info("🛑 AI买手助手后端关闭中...")
    await close_db()

app = FastAPI(title="AI Fashion Buyer API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(routes.router, prefix="/api/v1", tags=["API"])

@app.get("/")
def root(): return {"name": "AI Fashion Buyer API", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health(): return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
