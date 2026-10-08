from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat, conversation, knowledge_base, health
from app.database import Base, engine
from app.config import settings
from app.utils.logger import logger, log_api_request, log_api_response
import time

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于 LangChain 的 RAG 企业级知识库问答系统"
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有 API 请求和响应"""
    start_time = time.time()

    # 记录请求
    logger.info(f"Request: {request.method} {request.url.path}")

    # 处理请求
    response = await call_next(request)

    # 计算耗时
    duration = (time.time() - start_time) * 1000

    # 记录响应
    logger.info(f"Response: {request.url.path} | Status: {response.status_code} | Duration: {duration:.2f}ms")

    return response

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(conversation.router)
app.include_router(knowledge_base.router)


@app.get("/")
async def root():
    return {
        "message": "RAG Knowledge Base API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
