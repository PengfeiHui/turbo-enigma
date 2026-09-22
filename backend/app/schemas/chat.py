from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageSource(BaseModel):
    """引用来源"""
    content: str
    score: float


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[MessageSource]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    conversation_id: int


class ChatStreamChunk(BaseModel):
    chunk: str
    done: bool = False


class ConversationCreate(BaseModel):
    title: Optional[str] = "新对话"


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int
