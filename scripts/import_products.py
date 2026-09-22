"""
商品数据导入脚本
将爬取的商品数据导入到向量数据库
"""
import sys
import os
import json
import asyncio

# 添加 backend 目录到 Python 路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from app.services.vector_store_service import vector_store_service
from app.utils.text_splitter import split_text


async def import_products(json_file="crawler/output/products.json"):
    """导入商品数据到向量库"""
    print("📚 开始导入商品数据到向量库...")

    # 构建完整路径
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(project_root, json_file)

    # 读取 JSON 文件
    if not os.path.exists(json_path):
        print(f"❌ 文件不存在: {json_path}")
        print(f"💡 请先运行爬虫生成数据:")
        print(f"   cd crawler")
        print(f"   python pdd_crawler.py")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"📦 共有 {len(products)} 个商品待导入")

    # 构建文档
    texts = []
    metadatas = []

    for i, product in enumerate(products, 1):
        # 构建商品文档文本
        doc_text = f"""商品名称：{product.get('title', '未知')}
价格：¥{product.get('price', '0')}
原价：¥{product.get('original_price', product.get('price', '0'))}
销量：{product.get('sales', '0')}
分类：{product.get('category', '未分类')}
商品描述：{product.get('description', product.get('title', ''))}
商品链接：{product.get('url', '')}"""

        # 对于较长的文本，进行分割
        if len(doc_text) > 500:
            chunks = split_text(doc_text)
            for j, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "product_id": product.get('product_id', f'product_{i}'),
                    "title": product.get('title', ''),
                    "price": product.get('price', ''),
                    "category": product.get('category', ''),
                    "chunk_index": j,
                    "total_chunks": len(chunks)
                })
        else:
            texts.append(doc_text)
            metadatas.append({
                "product_id": product.get('product_id', f'product_{i}'),
                "title": product.get('title', ''),
                "price": product.get('price', ''),
                "category": product.get('category', ''),
                "chunk_index": 0,
                "total_chunks": 1
            })

        if i % 10 == 0:
            print(f"处理中... {i}/{len(products)}")

    print(f"✅ 文本处理完成，共 {len(texts)} 个文本块")

    # 批量导入向量库
    try:
        print("🔄 正在向量化并存入数据库...")
        await vector_store_service.add_documents(texts, metadatas)
        print(f"✅ 导入成功！{len(texts)} 个文本块已存入向量库")

        # 显示统计信息
        count = vector_store_service.get_collection_count()
        print(f"📊 向量库当前总文档数: {count}")
        print("")
        print("现在可以启动项目并进行问答了！")

    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(import_products())
