import random
from sqlalchemy.orm import Session
from app.models.user import User


def generate_unique_account(db: Session) -> str:
    """生成唯一的 11 位数字账号

    格式：第一位不为 0，后面 10 位随机数字
    例如：10234567890
    """
    max_attempts = 100  # 最多尝试 100 次

    for _ in range(max_attempts):
        # 第一位：1-9
        first_digit = random.randint(1, 9)

        # 后 10 位：0-9
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])

        # 组合成 11 位账号
        account = str(first_digit) + remaining_digits

        # 检查是否已存在
        existing = db.query(User).filter(User.account == account).first()
        if not existing:
            return account

    # 如果 100 次都失败（极小概率），抛出异常
    raise ValueError("无法生成唯一账号，请稍后重试")


def validate_username(username: str) -> tuple[bool, str]:
    """验证用户名格式

    规则：
    - 长度：2-20 个字符
    - 允许：中文、英文、数字、下划线
    - 不允许：纯数字（避免与账号混淆）

    Returns:
        (是否有效, 错误信息)
    """
    # 检查长度
    if len(username) < 2 or len(username) > 20:
        return False, "用户名长度必须在 2-20 个字符之间"

    # 检查是否为纯数字
    if username.isdigit():
        return False, "用户名不能为纯数字"

    # 检查字符（中文、英文、数字、下划线）
    import re
    pattern = r'^[一-龥a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, "用户名只能包含中文、英文、数字和下划线"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """验证密码格式

    规则：
    - 长度：6-20 个字符
    - 必须包含：字母和数字

    Returns:
        (是否有效, 错误信息)
    """
    # 检查长度
    if len(password) < 6 or len(password) > 20:
        return False, "密码长度必须在 6-20 个字符之间"

    # 检查是否包含字母
    has_letter = any(c.isalpha() for c in password)
    if not has_letter:
        return False, "密码必须包含字母"

    # 检查是否包含数字
    has_digit = any(c.isdigit() for c in password)
    if not has_digit:
        return False, "密码必须包含数字"

    return True, ""
