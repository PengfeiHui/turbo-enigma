from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """获取文本分割器"""
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    )


def split_text(text: str) -> list[str]:
    """分割文本"""
    splitter = get_text_splitter()
    chunks = splitter.split_text(text)
    return chunks
