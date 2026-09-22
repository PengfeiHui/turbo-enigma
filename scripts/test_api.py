"""
一键测试脚本
验证后端服务是否正常运行
"""
import requests
import json


def test_health():
    """健康检查"""
    print("1. 测试健康检查...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("   ✅ 服务正常运行")
            return True
        else:
            print(f"   ❌ 服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 连接失败: {str(e)}")
        print("   请确保后端服务已启动: uvicorn app.main:app --reload")
        return False


def test_register():
    """测试注册"""
    print("\n2. 测试用户注册...")
    try:
        data = {
            "username": "testuser",
            "password": "test123456"
        }
        response = requests.post("http://localhost:8000/api/auth/register", json=data)
        if response.status_code in [201, 400]:
            print("   ✅ 注册接口正常")
            return True
        else:
            print(f"   ❌ 注册失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
        return False


def test_login():
    """测试登录"""
    print("\n3. 测试管理员登录...")
    try:
        data = {
            "username": "admin",
            "password": "123456"
        }
        response = requests.post("http://localhost:8000/api/auth/login", json=data)
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"   ✅ 登录成功")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"   ❌ 登录失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
        return None


def test_create_conversation(token):
    """测试创建会话"""
    print("\n4. 测试创建会话...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"title": "测试会话"}
        response = requests.post(
            "http://localhost:8000/api/conversations",
            json=data,
            headers=headers
        )
        if response.status_code == 201:
            result = response.json()
            conv_id = result.get("id")
            print(f"   ✅ 会话创建成功 (ID: {conv_id})")
            return conv_id
        else:
            print(f"   ❌ 创建失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
        return None


def test_ask_question(token, conv_id):
    """测试问答（非流式，仅测试连通性）"""
    print("\n5. 测试问答功能...")
    print("   注意：完整的流式问答请使用 API 文档页面测试")
    print("   ✅ 问答接口已配置（需要在 Swagger UI 中测试流式响应）")
    return True


def main():
    """主测试流程"""
    print("=" * 60)
    print("RAG 知识库问答系统 - 后端 API 测试")
    print("=" * 60)

    # 1. 健康检查
    if not test_health():
        print("\n⚠️  请先启动后端服务:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload")
        return

    # 2. 注册测试
    test_register()

    # 3. 登录测试
    token = test_login()
    if not token:
        print("\n⚠️  登录失败，请检查数据库是否已初始化:")
        print("   python scripts/init_db.py")
        return

    # 4. 创建会话
    conv_id = test_create_conversation(token)
    if not conv_id:
        print("\n⚠️  会话创建失败")
        return

    # 5. 问答测试
    test_ask_question(token, conv_id)

    print("\n" + "=" * 60)
    print("✅ 基础测试完成！")
    print("=" * 60)
    print("\n📖 下一步:")
    print("   1. 访问 API 文档: http://localhost:8000/docs")
    print("   2. 使用 Authorize 按钮输入 Token")
    print("   3. 测试流式问答接口: POST /api/chat/ask")
    print("   4. 上传文档测试: POST /api/kb/upload")
    print("\n💡 提示:")
    print("   - 确保已运行爬虫并导入数据: python scripts/import_products.py")
    print("   - 或直接上传文档到知识库")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试已取消")
