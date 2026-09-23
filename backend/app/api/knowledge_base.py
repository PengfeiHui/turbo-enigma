import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import admin_required
from app.models.user import User
from app.models.knowledge_base import KnowledgeBase
from app.models.document import Document
from app.schemas.knowledge_base import (
    KnowledgeBaseCreate, KnowledgeBaseResponse,
    DocumentResponse, DocumentListResponse, UploadResponse
)
from app.services.document_processor import document_processor
from app.services.vector_store_service import vector_store_service
from app.utils.text_splitter import split_text
from app.config import settings

router = APIRouter(prefix="/api/kb", tags=["知识库管理"])


@router.post("/knowledge-bases", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(
    data: KnowledgeBaseCreate,
    admin_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """创建知识库（仅管理员）"""
    kb = KnowledgeBase(
        name=data.name,
        description=data.description
    )
    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb


@router.get("/knowledge-bases", response_model=List[KnowledgeBaseResponse])
async def get_knowledge_bases(
    admin_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """获取所有知识库（仅管理员）"""
    kbs = db.query(KnowledgeBase).all()
    return kbs


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    kb_id: int = 1,  # 默认知识库 ID
    admin_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """上传文档到知识库（仅管理员）"""
    # 检查文件大小
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大 {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB）"
        )

    # 检查知识库是否存在
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识库不存在"
        )

    try:
        # 1. 提取文本
        text = await document_processor.extract_text(file.filename, file.file)

        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文档内容为空或太短"
            )

        # 2. 文本分割
        chunks = split_text(text)

        # 3. 构建元数据
        metadatas = [
            {
                "filename": file.filename,
                "kb_id": kb_id,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        # 4. 添加到向量库
        await vector_store_service.add_documents(chunks, metadatas)

        # 5. 保存文档到上传目录
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)

        # 6. 记录到数据库
        document = Document(
            kb_id=kb_id,
            filename=file.filename,
            file_path=file_path,
            chunk_count=len(chunks)
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        return UploadResponse(
            message="文档上传成功",
            document_id=document.id,
            filename=file.filename,
            chunk_count=len(chunks)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文档处理失败: {str(e)}"
        )


@router.get("/documents", response_model=DocumentListResponse)
async def get_documents(
    kb_id: int = None,
    admin_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """获取文档列表（仅管理员）"""
    query = db.query(Document)
    if kb_id:
        query = query.filter(Document.kb_id == kb_id)

    documents = query.order_by(Document.created_at.desc()).all()
    return DocumentListResponse(
        documents=[DocumentResponse.from_orm(doc) for doc in documents],
        total=len(documents)
    )


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    admin_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """删除文档（仅管理员）"""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )

    try:
        # 1. 从向量库删除（失败不影响后续删除）
        try:
            await vector_store_service.delete_by_metadata({"filename": document.filename})
            print(f"✓ 向量库删除成功: {document.filename}")
        except Exception as e:
            print(f"⚠ 向量库删除失败（继续执行）: {str(e)}")

        # 2. 删除物理文件（失败不影响数据库删除）
        try:
            if document.file_path and os.path.exists(document.file_path):
                os.remove(document.file_path)
                print(f"✓ 文件删除成功: {document.file_path}")
        except Exception as e:
            print(f"⚠ 文件删除失败（继续执行）: {str(e)}")

        # 3. 从数据库删除（这是最重要的）
        db.delete(document)
        db.commit()
        print(f"✓ 数据库删除成功: {document.filename}")

        return None

    except Exception as e:
        db.rollback()
        print(f"✗ 删除失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )
