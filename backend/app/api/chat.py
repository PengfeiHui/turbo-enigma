import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.schemas.chat import ChatRequest
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/chat", tags=["问答"])


@router.post("/ask")
async def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """流式问答接口（Server-Sent Events）"""
    # 验证会话所有权
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    # 更新会话时间
    from sqlalchemy import func
    conversation.updated_at = func.now()
    db.commit()

    # 流式生成响应
    async def event_stream():
        try:
            async for chunk in rag_service.ask_question(
                question=request.question,
                conversation_id=request.conversation_id,
                db=db
            ):
                # SSE 格式
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"

            # 发送完成信号
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
        except Exception as e:
            error_msg = f"data: {json.dumps({'error': str(e)})}\n\n"
            yield error_msg

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
