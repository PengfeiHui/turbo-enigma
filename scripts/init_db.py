"""
数据库初始化脚本
创建表结构并初始化管理员账户
"""
import sys
import os

# 添加 backend 目录到 Python 路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.database import engine, SessionLocal, Base
from app.models import User, Conversation, Message, KnowledgeBase, Document
from app.utils.security import get_password_hash


def init_database():
    """初始化数据库"""
    print("🔧 开始初始化数据库...")

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 检查管理员是否已存在
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("⚠️  管理员账户已存在，跳过创建")
        else:
            # 创建管理员账户
            admin = User(
                username="admin",
                password_hash=get_password_hash("123456"),
                role="admin"
            )
            db.add(admin)
            print("✅ 创建管理员账户: admin / 123456")

        # 创建默认知识库
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == 1).first()
        if not kb:
            kb = KnowledgeBase(
                name="电商商品知识库",
                description="拼多多商品信息知识库"
            )
            db.add(kb)
            print("✅ 创建默认知识库")

        db.commit()
        print("✅ 数据库初始化完成！")
        print("")
        print("现在可以启动后端服务了:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        print("")
        print("或者双击运行: start-backend.bat")

    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
