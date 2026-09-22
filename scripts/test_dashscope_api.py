"""
测试阿里百炼 API 连接
"""
import os
import sys

# 添加 backend 目录到路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.config import settings

def test_api_key():
    """测试 API Key 配置"""
    print("=" * 60)
    print("测试阿里百炼 API 配置")
    print("=" * 60)
    print()

    print(f"API Key: {settings.DASHSCOPE_API_KEY[:20]}...{settings.DASHSCOPE_API_KEY[-10:]}")
    print(f"模型: {settings.LLM_MODEL}")
    print()

    print("尝试调用 API...")
    try:
        from langchain_community.llms import Tongyi

        llm = Tongyi(
            model_name=settings.LLM_MODEL,
            temperature=0.7,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )

        print("发送测试请求: '你好'")
        response = llm.invoke("你好，请简单介绍一下自己")

        print("\n✅ API 调用成功！")
        print(f"回复: {response}")
        print("\n✅ 阿里百炼 API 工作正常")

    except Exception as e:
        print(f"\n❌ API 调用失败")
        print(f"错误信息: {str(e)}")
        print()
        print("可能的原因:")
        print("1. API Key 不正确")
        print("2. 账户余额不足")
        print("3. 网络连接问题")
        print("4. API 限流")
        print()
        print("请检查:")
        print("- 登录 https://dashscope.aliyun.com/ 查看账户状态")
        print("- 确认 API Key 有效")
        print("- 检查网络连接")

if __name__ == "__main__":
    test_api_key()
