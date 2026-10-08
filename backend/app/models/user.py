from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)  # 用户名（昵称）
    account = Column(String(11), unique=True, nullable=False, index=True)  # 11位数字账号（登录用）
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # 'admin' or 'user'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
