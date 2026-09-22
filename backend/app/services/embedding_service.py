from typing import List
from langchain_community.embeddings import DashScopeEmbeddings
from app.config import settings


class EmbeddingService:
    """阿里百炼 Embedding 服务"""

    def __init__(self):
        self.embeddings = DashScopeEmbeddings(
            model=settings.EMBEDDING_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )

    async def embed_query(self, text: str) -> List[float]:
        """查询文本向量化"""
        return await self.embeddings.aembed_query(text)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量文档向量化"""
        return await self.embeddings.aembed_documents(texts)


# 全局单例
embedding_service = EmbeddingService()
