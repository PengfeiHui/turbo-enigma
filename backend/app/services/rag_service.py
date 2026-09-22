from typing import AsyncIterator, List, Tuple
from sqlalchemy.orm import Session
from app.models.message import Message
from app.services.llm_service import llm_service
from app.services.vector_store_service import vector_store_service
from app.schemas.chat import MessageSource


class RAGService:
    """RAG 核心服务"""

    async def ask_question(
        self,
        question: str,
        conversation_id: int,
        db: Session
    ) -> AsyncIterator[str]:
        """
        RAG 问答流程：
        1. 获取历史消息构建上下文
        2. 向量检索相关文档
        3. 构建 Prompt（包含历史对话）
        4. 流式生成回答
        5. 保存消息到数据库
        """
        # 1. 获取最近的历史消息（最多 10 条，5 轮对话）
        history_messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(10).all()

        # 反转顺序，使其按时间正序排列
        history_messages.reverse()

        # 构建历史对话文本
        history_context = ""
        if history_messages:
            history_parts = []
            for msg in history_messages:
                role_name = "用户" if msg.role == "user" else "助手"
                history_parts.append(f"{role_name}：{msg.content}")
            history_context = "\n".join(history_parts)

        # 2. 向量检索相关文档（Top-K）
        docs_with_scores = await vector_store_service.similarity_search_with_score(
            question, k=5
        )

        # 2. 构建上下文
        if not docs_with_scores:
            context = "暂无相关商品信息。"
            sources = []
        else:
            context_parts = []
            sources = []
            for i, (doc, score) in enumerate(docs_with_scores, 1):
                context_parts.append(f"[商品{i}]\n{doc.page_content}")
                sources.append({
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata
                })
            context = "\n\n".join(context_parts)

        # 3. 构建 Prompt（包含历史对话）
        if history_context:
            prompt = f"""你是一个专业的电商客服助手。请基于以下信息回答用户问题。

【历史对话】
{history_context}

【知识库信息】
{context}

【回答要求】
1. 根据历史对话理解上下文，保持对话连贯性
2. 如果用户提到"它"、"这个"、"刚才那个"等代词，结合历史对话理解指代内容
3. 优先使用知识库信息回答，确保准确性
4. 如果知识库中没有相关内容，可以基于历史对话做出合理推断
5. 回答要自然、友好，像真人客服一样

【当前问题】
用户：{question}

请回答："""
        else:
            prompt = f"""你是一个专业的电商客服助手。请基于以下商品信息回答用户问题。

要求：
1. 如果商品信息中包含用户问题的答案，请准确、详细地回答
2. 如果信息不足或找不到相关商品，礼貌地告知用户
3. 回答要自然、友好，像真人客服一样
4. 可以引用具体的商品信息，但不要生编虚假内容

商品信息：
{context}

用户问题：{question}

请回答："""

        # 5. 流式生成回答
        answer_chunks = []
        async for chunk in llm_service.generate_stream(prompt):
            answer_chunks.append(chunk)
            yield chunk

        # 6. 保存到数据库
        full_answer = "".join(answer_chunks)

        # 保存用户消息
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=question,
            sources=None
        )
        db.add(user_message)

        # 保存助手回复
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_answer,
            sources=sources if sources else None
        )
        db.add(assistant_message)
        db.commit()


# 全局单例
rag_service = RAGService()
