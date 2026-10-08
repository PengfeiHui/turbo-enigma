from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.utils.account_generator import generate_unique_account, validate_username, validate_password


class AuthService:
    """认证服务"""

    @staticmethod
    def authenticate_user(db: Session, account: str, password: str) -> tuple[User | None, str]:
        """验证用户登录（使用账号登录）

        特殊处理：admin 可以直接作为账号登录

        Returns:
            tuple: (user, error_message)
            - 成功: (User对象, "")
            - 账号不存在: (None, "account_not_found")
            - 密码错误: (None, "wrong_password")
        """
        # 特殊处理：如果账号是 "admin"，则查找 username 为 admin 的用户
        if account == "admin":
            user = db.query(User).filter(User.username == "admin").first()
        else:
            user = db.query(User).filter(User.account == account).first()

        if not user:
            return None, "account_not_found"
        if not verify_password(password, user.password_hash):
            return None, "wrong_password"
        return user, ""

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str = "user") -> User:
        """创建用户

        Args:
            username: 用户名（昵称）
            password: 密码
            role: 角色

        Returns:
            User: 创建的用户对象
        """
        # 验证用户名格式
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            raise ValueError(error_msg)

        # 验证密码格式
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            raise ValueError(error_msg)

        # 生成唯一的 11 位数字账号
        account = generate_unique_account(db)

        # 创建用户
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            account=account,
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

        # 验证新密码格式
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            raise ValueError(error_msg)

        user.password_hash = get_password_hash(new_password)
        db.commit()
        return True

    @staticmethod
    def generate_token(user: User) -> str:
        """生成 JWT Token（使用账号作为标识）"""
        return create_access_token(data={"sub": user.account})


# 全局单例
auth_service = AuthService()
