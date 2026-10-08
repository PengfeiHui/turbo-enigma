import os
from typing import List, Tuple, Optional
import hashlib
from langchain.vectorstores import Chroma
from langchain.schema import Document
from app.config import settings
from app.services.embedding_service import embedding_service
from app.utils.logger import logger


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

        # 简单的内存缓存（生产环境建议使用 Redis）
        self._cache = {}
        self._cache_max_size = 100

    def _get_cache_key(self, query: str, k: int) -> str:
        """生成缓存键"""
        cache_str = f"{query}:{k}"
        return hashlib.md5(cache_str.encode()).hexdigest()

    def _get_from_cache(self, key: str) -> Optional[List[Tuple[Document, float]]]:
        """从缓存获取"""
        return self._cache.get(key)

    def _set_cache(self, key: str, value: List[Tuple[Document, float]]):
        """设置缓存"""
        # 简单的 LRU 策略：缓存满了删除最早的
        if len(self._cache) >= self._cache_max_size:
            # 删除第一个键（最早添加的）
            first_key = next(iter(self._cache))
            del self._cache[first_key]

        self._cache[key] = value

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()

    async def add_documents(self, texts: List[str], metadatas: List[dict]) -> List[str]:
        """添加文档到向量库"""
        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]
        ids = await self.vectorstore.aadd_documents(documents)
        self.vectorstore.persist()

        # 添加新文档后清空缓存
        self.clear_cache()

        return ids

    async def similarity_search_with_score(
        self, query: str, k: int = 5
    ) -> List[Tuple[Document, float]]:
        """相似度搜索（带分数）- 带缓存"""
        # 生成缓存键
        cache_key = self._get_cache_key(query, k)

        # 尝试从缓存获取
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            logger.info(f"✓ 缓存命中: {query[:30]}...")
            return cached_result

        # 缓存未命中，执行查询
        logger.info(f"⚡ 执行向量查询: {query[:30]}...")
        results = await self.vectorstore.asimilarity_search_with_score(query, k=k)

        # 保存到缓存
        self._set_cache(cache_key, results)

        return results

    async def delete_by_metadata(self, metadata_filter: dict):
        """根据元数据删除文档"""
        try:
            # Chroma 的 where 参数需要完整的过滤条件
            # 格式：{"metadata_field": {"$eq": "value"}}
            where_filter = {}
            for key, value in metadata_filter.items():
                where_filter[key] = {"$eq": value}

            # 使用同步方法删除（Chroma 不支持异步删除）
            self.vectorstore._collection.delete(where=where_filter)
            self.vectorstore.persist()

            # 删除文档后清空缓存
            self.clear_cache()

        except Exception as e:
            logger.error(f"删除向量失败: {str(e)}")
            # 即使向量删除失败，也不应该阻止文档删除
            pass

    def get_collection_count(self) -> int:
        """获取集合中的文档数量"""
        return self.vectorstore._collection.count()


# 全局单例
vector_store_service = VectorStoreService()
