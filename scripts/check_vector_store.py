"""
检查向量库状态
"""
import os
import sys

# 添加 backend 目录到路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.services.vector_store_service import vector_store_service

def check_vector_store():
    """检查向量库状态"""
    print("=" * 60)
    print("检查向量库状态")
    print("=" * 60)
    print()

    try:
        count = vector_store_service.get_collection_count()
        print(f"📊 向量库文档数量: {count}")
        print()

        if count == 0:
            print("⚠️  向量库为空！")
            print()
            print("原因：知识库中还没有任何文档")
            print()
            print("解决方案：")
            print("1. 生成测试文档:")
            print("   python scripts\\generate_test_docs.py")
            print()
            print("2. 通过前端上传文档:")
            print("   - 访问 http://localhost:5173")
            print("   - 登录 admin/123456")
            print("   - 点击左下角 → 知识库管理")
            print("   - 上传 test_documents 目录下的 .txt 文件")
            print()
            print("3. 或使用爬虫导入数据:")
            print("   cd crawler")
            print("   python pdd_crawler.py")
            print("   cd ..")
            print("   python scripts\\import_products.py")
        else:
            print("✅ 向量库有数据！")
            print()
            print("你可以问这些问题:")
            print("- '有什么好的蓝牙耳机推荐？'")
            print("- '推荐几款1000元左右的充电宝'")
            print("- '华为 Mate 60 Pro 的主要特点是什么？'")

    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_vector_store()
