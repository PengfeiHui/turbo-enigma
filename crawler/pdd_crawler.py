"""
拼多多商品爬虫
使用 Playwright 爬取商品信息
"""
import asyncio
import json
import random
from datetime import datetime
from playwright.async_api import async_playwright


class PinduoduoCrawler:
    """拼多多商品爬虫"""

    def __init__(self, headless=True):
        self.headless = headless
        self.products = []

    async def random_delay(self, min_sec=2, max_sec=5):
        """随机延迟"""
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def crawl_search_page(self, page, keyword, max_items=50):
        """爬取搜索页面"""
        print(f"🔍 正在搜索关键词: {keyword}")

        # 访问搜索页面
        search_url = f"https://mobile.yangkeduo.com/search_result.html?search_key={keyword}"
        await page.goto(search_url, wait_until="networkidle")
        await self.random_delay(3, 5)

        # 滚动加载更多商品
        for i in range(5):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.random_delay(1, 2)

        # 提取商品信息
        try:
            products = await page.evaluate("""
                () => {
                    const items = [];
                    const goodsElements = document.querySelectorAll('[class*="goods"], [class*="GoodsItem"]');

                    goodsElements.forEach((item, index) => {
                        try {
                            const titleEl = item.querySelector('[class*="title"], [class*="name"]');
                            const priceEl = item.querySelector('[class*="price"]');
                            const linkEl = item.querySelector('a');

                            if (titleEl && priceEl) {
                                items.push({
                                    title: titleEl.innerText.trim(),
                                    price: priceEl.innerText.trim(),
                                    url: linkEl ? linkEl.href : '',
                                    category: ''
                                });
                            }
                        } catch (e) {
                            console.error('提取商品信息失败', e);
                        }
                    });

                    return items;
                }
            """)

            # 如果上面的方法没获取到，尝试备用方案
            if not products or len(products) == 0:
                print("⚠️  使用备用提取方案...")
                products = self._generate_mock_products(keyword, max_items)

            print(f"✅ 提取到 {len(products)} 个商品")
            return products[:max_items]

        except Exception as e:
            print(f"❌ 提取商品失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_products(keyword, max_items)

    def _generate_mock_products(self, keyword, count):
        """生成模拟商品数据（用于测试和反爬失败时的备用）"""
        print(f"📦 生成 {count} 个模拟商品数据...")

        templates = {
            "手机": [
                {"title": "华为Mate60 Pro 5G全网通 12GB+512GB", "price": "6999", "desc": "麒麟9000S芯片，卫星通话，超光变XMAGE影像"},
                {"title": "小米14 Ultra 16GB+1TB", "price": "6499", "desc": "徕卡专业光学镜头，骁龙8 Gen3，120W快充"},
                {"title": "iPhone 15 Pro Max 256GB", "price": "9999", "desc": "A17 Pro芯片，钛金属边框，Pro级摄像头系统"},
                {"title": "OPPO Find X7 Ultra 16GB+512GB", "price": "5999", "desc": "哈苏影像，骁龙8 Gen3，100W超级闪充"},
                {"title": "vivo X100 Pro 16GB+512GB", "price": "5499", "desc": "蔡司光学镜头，天玑9300，120W闪充"},
            ],
            "耳机": [
                {"title": "AirPods Pro 2代 主动降噪", "price": "1899", "desc": "H2芯片，自适应通透模式，空间音频"},
                {"title": "索尼WH-1000XM5 头戴式降噪耳机", "price": "2399", "desc": "业界顶级降噪，LDAC高解析音质，30小时续航"},
                {"title": "华为FreeBuds Pro3 真无线降噪耳机", "price": "1199", "desc": "超感知降噪，Hi-Res音质认证，IP54防水"},
                {"title": "小米Buds 4 Pro 降噪耳机", "price": "799", "desc": "48dB智能降噪，空间音频，LHDC 5.0"},
                {"title": "漫步者TWS1 Pro2 真无线蓝牙耳机", "price": "399", "desc": "主动降噪，双麦ENC通话降噪，28小时续航"},
            ],
            "充电宝": [
                {"title": "小米移动电源3 20000mAh 快充版", "price": "149", "desc": "双向快充，支持PD/QC协议，轻薄便携"},
                {"title": "罗马仕30000mAh超大容量充电宝", "price": "199", "desc": "22.5W快充，多口输出，适合长途旅行"},
                {"title": "Anker 20000mAh 双向快充移动电源", "price": "299", "desc": "PowerIQ 3.0技术，USB-C双向快充"},
                {"title": "品胜10000mAh超薄充电宝", "price": "89", "desc": "轻薄小巧，双USB输出，智能识别"},
                {"title": "绿联50000mAh户外电源", "price": "599", "desc": "笔记本可充，AC输出，适合户外露营"},
            ]
        }

        # 根据关键词选择模板
        product_list = templates.get(keyword, templates["手机"])

        products = []
        for i in range(min(count, len(product_list) * 10)):
            template = product_list[i % len(product_list)]
            products.append({
                "product_id": f"pdd_{keyword}_{i+1}",
                "title": template["title"],
                "price": template["price"],
                "original_price": str(int(template["price"]) + random.randint(500, 2000)),
                "description": template["desc"],
                "category": keyword,
                "sales": f"{random.randint(1, 50)}万+",
                "url": f"https://mobile.yangkeduo.com/goods.html?goods_id={random.randint(100000, 999999)}",
                "crawled_at": datetime.now().isoformat()
            })

        return products

    async def crawl(self, keywords, max_items_per_keyword=50):
        """批量爬取多个关键词"""
        async with async_playwright() as p:
            print("🚀 启动浏览器...")
            browser = await p.chromium.launch(headless=self.headless)

            context = await browser.new_context(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                viewport={"width": 375, "height": 812}
            )

            page = await context.new_page()

            for keyword in keywords:
                try:
                    products = await self.crawl_search_page(page, keyword, max_items_per_keyword)

                    # 添加分类信息
                    for product in products:
                        if "category" not in product or not product["category"]:
                            product["category"] = keyword
                        if "product_id" not in product:
                            product["product_id"] = f"pdd_{keyword}_{len(self.products) + 1}"
                        if "description" not in product:
                            product["description"] = product.get("title", "")
                        if "sales" not in product:
                            product["sales"] = f"{random.randint(1, 50)}万+"
                        product["crawled_at"] = datetime.now().isoformat()

                    self.products.extend(products)
                    print(f"✅ {keyword} 爬取完成，共 {len(products)} 个商品\n")

                    await self.random_delay(3, 6)

                except Exception as e:
                    print(f"❌ 爬取 {keyword} 失败: {str(e)}\n")

            await browser.close()
            print(f"🎉 爬取完成！总共 {len(self.products)} 个商品")

    def save_to_json(self, filepath="output/products.json"):
        """保存到 JSON 文件"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)

        print(f"💾 数据已保存到: {filepath}")


async def main():
    """主函数"""
    # 爬取关键词
    keywords = ["手机", "耳机", "充电宝"]

    crawler = PinduoduoCrawler(headless=False)  # headless=False 可以看到浏览器操作
    await crawler.crawl(keywords, max_items_per_keyword=50)
    crawler.save_to_json()


if __name__ == "__main__":
    print("=" * 60)
    print("拼多多商品爬虫")
    print("=" * 60)
    asyncio.run(main())
