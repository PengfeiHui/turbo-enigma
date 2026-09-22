"""
调试流式输出
直接测试 RAG 服务的输出
"""
import os
import sys
import asyncio

# 添加 backend 目录到路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

async def test_streaming():
    """测试流式输出"""
    print("=" * 60)
    print("测试流式问答输出")
    print("=" * 60)
    print()

    from app.services.llm_service import llm_service

    question = "你好，请介绍一下自己"
    print(f"问题: {question}")
    print()
    print("流式输出:")
    print("-" * 60)

    chunks = []
    try:
        async for chunk in llm_service.generate_stream(question):
            print(chunk, end='', flush=True)
            chunks.append(chunk)
    except Exception as e:
        print(f"\n\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return

    print()
    print("-" * 60)
    print()
    print(f"✅ 共接收到 {len(chunks)} 个文本块")
    print(f"✅ 完整回答长度: {len(''.join(chunks))} 字符")
    print()
    print("完整回答:")
    print(''.join(chunks))

if __name__ == "__main__":
    asyncio.run(test_streaming())
