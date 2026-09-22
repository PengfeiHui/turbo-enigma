from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "RAG Knowledge Base"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str
    REDIS_URL: str

    # 阿里百炼 API
    DASHSCOPE_API_KEY: str

    # JWT 配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # Chroma 配置
    CHROMA_PERSIST_DIR: str = "../data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "product_knowledge"

    # 上传配置
    UPLOAD_DIR: str = "../data/uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    # RAG 配置
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    RETRIEVAL_TOP_K: int = 5

    # LLM 配置
    LLM_MODEL: str = "qwen-plus"
    LLM_TEMPERATURE: float = 0.7
    EMBEDDING_MODEL: str = "text-embedding-v2"

    class Config:
        # 自动查找 backend 目录下的 .env 文件
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
