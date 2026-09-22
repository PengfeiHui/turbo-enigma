import os
from typing import BinaryIO
import PyPDF2
import docx
from app.config import settings


class DocumentProcessor:
    """文档处理器：解析各类文档"""

    @staticmethod
    async def extract_text_from_pdf(file: BinaryIO) -> str:
        """从 PDF 提取文本"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"PDF 解析失败: {str(e)}")

    @staticmethod
    async def extract_text_from_docx(file: BinaryIO) -> str:
        """从 DOCX 提取文本"""
        try:
            doc = docx.Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise ValueError(f"DOCX 解析失败: {str(e)}")

    @staticmethod
    async def extract_text_from_txt(file: BinaryIO) -> str:
        """从 TXT 提取文本"""
        try:
            content = file.read()
            # 尝试多种编码
            for encoding in ['utf-8', 'gbk', 'gb2312']:
                try:
                    return content.decode(encoding).strip()
                except UnicodeDecodeError:
                    continue
            raise ValueError("无法识别文件编码")
        except Exception as e:
            raise ValueError(f"TXT 解析失败: {str(e)}")

    @staticmethod
    async def extract_text(filename: str, file: BinaryIO) -> str:
        """根据文件扩展名提取文本"""
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.pdf':
            return await DocumentProcessor.extract_text_from_pdf(file)
        elif ext == '.docx':
            return await DocumentProcessor.extract_text_from_docx(file)
        elif ext == '.txt':
            return await DocumentProcessor.extract_text_from_txt(file)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")


# 全局单例
document_processor = DocumentProcessor()
