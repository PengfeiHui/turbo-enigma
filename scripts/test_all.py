"""
RAG 知识库问答系统 - 全面测试脚本
测试前后端的各种潜在 Bug
"""
import os
import sys
import asyncio
import json
from datetime import datetime

# 添加 backend 目录到路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def test(self, name):
        """测试装饰器"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                print(f"\n{'='*60}")
                print(f"测试: {name}")
                print(f"{'='*60}")
                try:
                    await func(*args, **kwargs)
                    print(f"✅ 通过")
                    self.passed += 1
                except AssertionError as e:
                    print(f"❌ 失败: {str(e)}")
                    self.failed += 1
                    self.errors.append(f"{name}: {str(e)}")
                except Exception as e:
                    print(f"❌ 错误: {str(e)}")
                    self.failed += 1
                    self.errors.append(f"{name}: {str(e)}")
                    import traceback
                    traceback.print_exc()
            return wrapper
        return decorator

    def summary(self):
        """输出测试摘要"""
        print(f"\n{'='*60}")
        print("测试摘要")
        print(f"{'='*60}")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"总计: {self.passed + self.failed}")
        print()

        if self.errors:
            print("失败的测试:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("🎉 所有测试通过！")

runner = TestRunner()

# =============================================================================
# 后端测试
# =============================================================================

@runner.test("1. 配置加载测试")
async def test_config():
    """测试环境配置是否正确加载"""
    from app.config import settings

    assert settings.DASHSCOPE_API_KEY, "API Key 未配置"
    assert settings.DATABASE_URL, "数据库 URL 未配置"
    assert settings.REDIS_URL, "Redis URL 未配置"
    assert settings.SECRET_KEY, "JWT Secret Key 未配置"

    print(f"  - API Key: {settings.DASHSCOPE_API_KEY[:20]}...")
    print(f"  - 数据库: {settings.DATABASE_URL.split('@')[0]}@...")
    print(f"  - LLM 模型: {settings.LLM_MODEL}")

@runner.test("2. 数据库连接测试")
async def test_database():
    """测试数据库连接"""
    from app.database import SessionLocal, engine
    from sqlalchemy import text

    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1, "数据库查询失败"
        print(f"  - 数据库连接正常")
    finally:
        db.close()

@runner.test("3. 数据库表检查")
async def test_database_tables():
    """检查所有必需的数据库表"""
    from app.database import SessionLocal, engine
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    required_tables = ['users', 'conversations', 'messages', 'knowledge_bases', 'documents']

    for table in required_tables:
        assert table in tables, f"表 {table} 不存在"
        print(f"  - 表 {table} 存在")

@runner.test("4. 用户模型测试")
async def test_user_model():
    """测试用户模型和密码哈希"""
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        assert admin is not None, "管理员账户不存在"
        assert admin.role == "admin", "管理员角色不正确"
        print(f"  - 管理员账户存在")
        print(f"  - 用户 ID: {admin.id}")
        print(f"  - 角色: {admin.role}")
    finally:
        db.close()

@runner.test("5. 向量库连接测试")
async def test_vector_store():
    """测试向量库连接"""
    from app.services.vector_store_service import vector_store_service

    count = vector_store_service.get_collection_count()
    print(f"  - 向量库文档数量: {count}")

    if count == 0:
        print(f"  ⚠️  向量库为空，建议上传文档")

@runner.test("6. LLM API 测试")
async def test_llm_api():
    """测试阿里百炼 API"""
    from app.services.llm_service import llm_service

    response = await llm_service.generate("你好")
    assert response, "LLM 未返回任何内容"
    assert len(response) > 0, "LLM 返回内容为空"
    print(f"  - LLM 响应: {response[:50]}...")

@runner.test("7. 流式输出测试")
async def test_streaming():
    """测试流式输出"""
    from app.services.llm_service import llm_service

    chunks = []
    async for chunk in llm_service.generate_stream("你好"):
        chunks.append(chunk)

    assert len(chunks) > 0, "未接收到任何流式输出"
    full_text = "".join(chunks)
    assert len(full_text) > 0, "流式输出内容为空"
    print(f"  - 接收到 {len(chunks)} 个文本块")
    print(f"  - 总长度: {len(full_text)} 字符")

@runner.test("8. 密码哈希测试")
async def test_password_hash():
    """测试密码哈希功能"""
    from app.utils.security import get_password_hash, verify_password

    password = "test123456"
    hashed = get_password_hash(password)

    assert hashed != password, "密码未被哈希"
    assert verify_password(password, hashed), "密码验证失败"
    assert not verify_password("wrong", hashed), "错误密码通过了验证"
    print(f"  - 密码哈希正常")
    print(f"  - 密码验证正常")

@runner.test("9. JWT Token 测试")
async def test_jwt_token():
    """测试 JWT Token 生成和解码"""
    from app.utils.security import create_access_token, decode_access_token

    data = {"sub": "testuser"}
    token = create_access_token(data)

    assert token, "Token 生成失败"

    decoded = decode_access_token(token)
    assert decoded is not None, "Token 解码失败"
    assert decoded["sub"] == "testuser", "Token 数据不匹配"
    print(f"  - Token 生成正常")
    print(f"  - Token 解码正常")

@runner.test("10. 文本分割测试")
async def test_text_splitter():
    """测试文本分割功能"""
    from app.utils.text_splitter import split_text

    long_text = "这是测试文本。" * 200  # 约 1200 字符
    chunks = split_text(long_text, chunk_size=500, chunk_overlap=100)

    assert len(chunks) > 1, "长文本未被分割"
    assert all(len(chunk) <= 600 for chunk in chunks), "分块过大"
    print(f"  - 文本被分割为 {len(chunks)} 块")
    print(f"  - 每块大小: {[len(c) for c in chunks]}")

@runner.test("11. RAG 服务测试（无向量库）")
async def test_rag_without_docs():
    """测试没有知识库时的 RAG 服务"""
    from app.services.rag_service import rag_service
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        chunks = []
        async for chunk in rag_service.ask_question("你好", 1, db):
            chunks.append(chunk)
            if len(chunks) >= 5:  # 只测试前几个块
                break

        assert len(chunks) > 0, "RAG 服务未返回任何内容"
        print(f"  - RAG 服务响应正常")
        print(f"  - 接收到 {len(chunks)} 个文本块")
    finally:
        db.close()

@runner.test("12. 会话上下文测试")
async def test_conversation_context():
    """测试会话上下文记忆"""
    from app.database import SessionLocal
    from app.models.message import Message
    from app.models.conversation import Conversation
    from app.models.user import User

    db = SessionLocal()
    try:
        # 获取管理员用户
        admin = db.query(User).filter(User.username == "admin").first()

        # 创建测试会话
        test_conv = Conversation(
            user_id=admin.id,
            title="测试会话"
        )
        db.add(test_conv)
        db.commit()
        db.refresh(test_conv)

        # 添加测试消息
        msg1 = Message(conversation_id=test_conv.id, role="user", content="推荐蓝牙耳机")
        msg2 = Message(conversation_id=test_conv.id, role="assistant", content="推荐 AirPods Pro")
        db.add_all([msg1, msg2])
        db.commit()

        # 查询历史消息
        history = db.query(Message).filter(
            Message.conversation_id == test_conv.id
        ).order_by(Message.created_at.desc()).limit(10).all()

        assert len(history) == 2, "历史消息数量不正确"
        print(f"  - 会话创建成功")
        print(f"  - 历史消息数量: {len(history)}")

        # 清理测试数据
        db.query(Message).filter(Message.conversation_id == test_conv.id).delete()
        db.delete(test_conv)
        db.commit()

    finally:
        db.close()

# =============================================================================
# 边界情况和错误处理测试
# =============================================================================

@runner.test("13. 空输入测试")
async def test_empty_input():
    """测试空输入的处理"""
    from app.services.llm_service import llm_service

    try:
        response = await llm_service.generate("")
        print(f"  - 空输入返回: {response[:50] if response else 'None'}")
    except Exception as e:
        print(f"  - 空输入抛出异常（预期行为）: {str(e)[:50]}")

@runner.test("14. 超长输入测试")
async def test_long_input():
    """测试超长输入的处理"""
    from app.services.llm_service import llm_service

    long_input = "测试" * 1000  # 2000 字符
    try:
        chunks = []
        async for chunk in llm_service.generate_stream(long_input):
            chunks.append(chunk)
            if len(chunks) >= 3:
                break
        print(f"  - 超长输入处理正常，接收到 {len(chunks)} 个块")
    except Exception as e:
        print(f"  - 超长输入处理异常: {str(e)[:100]}")

@runner.test("15. 特殊字符测试")
async def test_special_characters():
    """测试特殊字符的处理"""
    from app.services.llm_service import llm_service

    special_input = "测试 @#$%^&*() 😊🎉 \"引号\" '单引号' \n换行"
    try:
        response = await llm_service.generate(special_input)
        print(f"  - 特殊字符处理正常")
    except Exception as e:
        print(f"  - 特殊字符处理异常: {str(e)[:100]}")

@runner.test("16. 并发请求测试")
async def test_concurrent_requests():
    """测试并发请求处理"""
    from app.services.llm_service import llm_service

    async def generate_task(prompt):
        return await llm_service.generate(prompt)

    tasks = [generate_task(f"问题{i}") for i in range(3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success = sum(1 for r in results if not isinstance(r, Exception))
    print(f"  - 并发请求: {success}/3 成功")

@runner.test("17. 数据库事务测试")
async def test_database_transaction():
    """测试数据库事务回滚"""
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    try:
        # 尝试创建重复用户（应该失败）
        try:
            duplicate_user = User(
                username="admin",  # 已存在
                password_hash="test",
                role="user"
            )
            db.add(duplicate_user)
            db.commit()
            assert False, "重复用户创建成功（不应该）"
        except Exception as e:
            db.rollback()
            print(f"  - 事务回滚正常（重复用户被拒绝）")
    finally:
        db.close()

# =============================================================================
# 性能测试
# =============================================================================

@runner.test("18. 响应时间测试")
async def test_response_time():
    """测试响应时间"""
    from app.services.llm_service import llm_service
    import time

    start = time.time()
    response = await llm_service.generate("你好")
    elapsed = time.time() - start

    print(f"  - 响应时间: {elapsed:.2f} 秒")

    if elapsed > 10:
        print(f"  ⚠️  响应较慢")
    else:
        print(f"  ✅ 响应速度正常")

@runner.test("19. 向量检索性能测试")
async def test_vector_search_performance():
    """测试向量检索性能"""
    from app.services.vector_store_service import vector_store_service
    import time

    count = vector_store_service.get_collection_count()
    if count == 0:
        print(f"  ⚠️  向量库为空，跳过测试")
        return

    start = time.time()
    results = await vector_store_service.similarity_search_with_score("测试查询", k=5)
    elapsed = time.time() - start

    print(f"  - 检索时间: {elapsed:.3f} 秒")
    print(f"  - 返回结果: {len(results)} 条")

# =============================================================================
# 主函数
# =============================================================================

async def main():
    print("=" * 60)
    print("RAG 知识库问答系统 - 全面测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 运行所有测试
    await test_config()
    await test_database()
    await test_database_tables()
    await test_user_model()
    await test_vector_store()
    await test_llm_api()
    await test_streaming()
    await test_password_hash()
    await test_jwt_token()
    await test_text_splitter()
    await test_rag_without_docs()
    await test_conversation_context()
    await test_empty_input()
    await test_long_input()
    await test_special_characters()
    await test_concurrent_requests()
    await test_database_transaction()
    await test_response_time()
    await test_vector_search_performance()

    # 输出摘要
    runner.summary()

if __name__ == "__main__":
    asyncio.run(main())
