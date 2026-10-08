import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name: str = "longchain_rag") -> logging.Logger:
    """配置日志系统"""

    # 创建日志目录
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件处理器 - 所有日志
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 文件处理器 - 错误日志
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# 全局 logger
logger = setup_logger()


def log_api_request(endpoint: str, method: str, user_id: int = None):
    """记录 API 请求"""
    logger.info(f"API Request: {method} {endpoint} | User: {user_id or 'Anonymous'}")


def log_api_response(endpoint: str, status_code: int, duration_ms: float):
    """记录 API 响应"""
    logger.info(f"API Response: {endpoint} | Status: {status_code} | Duration: {duration_ms:.2f}ms")


def log_error(error: Exception, context: str = ""):
    """记录错误"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_document_upload(filename: str, user_id: int, chunks: int):
    """记录文档上传"""
    logger.info(f"Document uploaded: {filename} | User: {user_id} | Chunks: {chunks}")


def log_query(question: str, user_id: int, conversation_id: int):
    """记录用户查询"""
    logger.info(f"Query: '{question[:50]}...' | User: {user_id} | Conversation: {conversation_id}")


def log_cache_hit(query: str):
    """记录缓存命中"""
    logger.debug(f"Cache HIT: {query[:30]}...")


def log_cache_miss(query: str):
    """记录缓存未命中"""
    logger.debug(f"Cache MISS: {query[:30]}...")
