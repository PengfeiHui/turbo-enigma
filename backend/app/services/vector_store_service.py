import os
from typing import List, Tuple
from langchain.vectorstores import Chroma
from langchain.schema import Document
from app.config import settings
from app.services.embedding_service import embedding_service


class VectorStoreService:
    """Chroma 向量数据库服务"""

    def __init__(self):
        # 确保持久化目录存在
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)

        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=embedding_service.embeddings,
            collection_name=settings.CHROMA_COLLECTION_NAME
        )

    async def add_documents(self, texts: List[str], metadatas: List[dict]) -> List[str]:
        """添加文档到向量库"""
        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]
        ids = await self.vectorstore.aadd_documents(documents)
        self.vectorstore.persist()
        return ids

    async def similarity_search_with_score(
        self, query: str, k: int = 5
    ) -> List[Tuple[Document, float]]:
        """相似度搜索（带分数）"""
        results = await self.vectorstore.asimilarity_search_with_score(query, k=k)
        return results

    async def delete_by_metadata(self, metadata_filter: dict):
        """根据元数据删除文档"""
        # Chroma 不直接支持异步删除，使用同步方法
        self.vectorstore.delete(where=metadata_filter)
        self.vectorstore.persist()

    def get_collection_count(self) -> int:
        """获取集合中的文档数量"""
        return self.vectorstore._collection.count()


# 全局单例
vector_store_service = VectorStoreService()
