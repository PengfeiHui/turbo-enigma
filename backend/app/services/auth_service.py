from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    """认证服务"""

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """验证用户登录"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str = "user") -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError("用户名已存在")

        # 创建用户
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            password_hash=hashed_password,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user: User, old_password: str, new_password: str) -> bool:
        """修改密码"""
        if not verify_password(old_password, user.password_hash):
            return False

        user.password_hash = get_password_hash(new_password)
        db.commit()
        return True

    @staticmethod
    def generate_token(user: User) -> str:
        """生成 JWT Token"""
        return create_access_token(data={"sub": user.username})


# 全局单例
auth_service = AuthService()
