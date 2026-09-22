"""
生成测试知识库文档
创建一些电商商品信息的测试文档
"""
import os
import random

# 创建输出目录
output_dir = "tests/documents"
os.makedirs(output_dir, exist_ok=True)

# 商品数据模板
products = {
    "手机": [
        {
            "name": "华为 Mate 60 Pro",
            "price": "6999",
            "features": ["麒麟9000S芯片", "卫星通话", "5000mAh大电池", "88W快充", "超光变XMAGE影像"],
            "description": "华为 Mate 60 Pro 是华为旗舰手机，搭载麒麟9000S芯片，支持卫星通话功能。配备6.82英寸OLED屏幕，120Hz刷新率。后置5000万像素主摄，支持10档可变光圈。内置5000mAh电池，支持88W有线快充和50W无线快充。"
        },
        {
            "name": "小米14 Ultra",
            "price": "6499",
            "features": ["骁龙8 Gen3", "徕卡光学镜头", "5000mAh电池", "120W快充", "2K屏幕"],
            "description": "小米14 Ultra 搭载高通骁龙8 Gen3处理器，配备徕卡专业光学镜头系统。6.73英寸2K AMOLED屏幕，支持120Hz刷新率。后置5000万像素主摄+5000万超广角+5000万长焦。5000mAh电池，支持120W有线快充和50W无线快充。"
        },
        {
            "name": "iPhone 15 Pro Max",
            "price": "9999",
            "features": ["A17 Pro芯片", "钛金属边框", "Action按钮", "潜望式长焦", "USB-C接口"],
            "description": "iPhone 15 Pro Max 采用3nm制程A17 Pro芯片，首次使用钛金属边框设计，重量更轻。配备6.7英寸超视网膜XDR显示屏。后置4800万像素主摄，支持5倍光学变焦的潜望式长焦镜头。改用USB-C接口，支持USB 3.0传输速度。"
        },
        {
            "name": "OPPO Find X7 Ultra",
            "price": "5999",
            "features": ["骁龙8 Gen3", "哈苏影像", "双潜望长焦", "5000mAh电池", "100W闪充"],
            "description": "OPPO Find X7 Ultra 搭载骁龙8 Gen3处理器，与哈苏联合调校影像系统。首创双潜望式长焦设计，分别支持3倍和6倍光学变焦。6.82英寸2K AMOLED屏幕，120Hz自适应刷新率。5000mAh电池，支持100W超级闪充。"
        },
        {
            "name": "vivo X100 Pro",
            "price": "5499",
            "features": ["天玑9300", "蔡司光学镜头", "蓝晶芯片", "5400mAh电池", "120W闪充"],
            "description": "vivo X100 Pro 搭载联发科天玑9300旗舰芯片，配备蔡司APO超级长焦镜头。自研蓝晶芯片技术栈，提升影像处理能力。6.78英寸2K AMOLED曲面屏，120Hz刷新率。5400mAh大电池，支持120W有线快充和50W无线快充。"
        }
    ],
    "耳机": [
        {
            "name": "AirPods Pro 2代",
            "price": "1899",
            "features": ["H2芯片", "主动降噪", "空间音频", "自适应通透", "30小时续航"],
            "description": "AirPods Pro 2代搭载全新H2芯片，主动降噪效果提升2倍。支持自适应通透模式，可智能调节环境音。个性化空间音频，支持动态头部追踪。单次续航6小时，配合充电盒总续航30小时。支持MagSafe充电和精确查找功能。"
        },
        {
            "name": "索尼 WH-1000XM5",
            "price": "2399",
            "features": ["业界顶级降噪", "LDAC高解析", "30小时续航", "多点连接", "舒适佩戴"],
            "description": "索尼WH-1000XM5是业界降噪标杆产品，采用全新设计的8个麦克风实现更强降噪。支持LDAC高解析音频传输，音质出色。30小时超长续航，快充3分钟可用3小时。支持多点连接，可同时连接两台设备。佩戴舒适，适合长时间使用。"
        },
        {
            "name": "华为 FreeBuds Pro 3",
            "price": "1199",
            "features": ["超感知降噪", "Hi-Res认证", "IP54防水", "31小时续航", "双设备连接"],
            "description": "华为FreeBuds Pro 3支持超感知降噪，可识别不同场景自动调节。通过Hi-Res Audio Wireless认证，音质优秀。IP54级防尘防水，适合运动使用。单次续航6.5小时，配合充电盒总续航31小时。支持双设备智慧连接。"
        },
        {
            "name": "小米 Buds 4 Pro",
            "price": "799",
            "features": ["48dB降噪", "空间音频", "LHDC 5.0", "无线充电", "38小时续航"],
            "description": "小米Buds 4 Pro提供最高48dB智能降噪深度，六麦克风通话降噪。支持小米空间音频和头部追踪。采用LHDC 5.0音频编码，音质更好。单次续航9小时，配合充电盒总续航38小时。支持无线充电和快充。"
        },
        {
            "name": "漫步者 TWS1 Pro2",
            "price": "399",
            "features": ["主动降噪", "双麦ENC", "28小时续航", "低延迟模式", "舒适佩戴"],
            "description": "漫步者TWS1 Pro2是性价比之选，支持主动降噪功能。双麦ENC通话降噪，通话清晰。配备10mm复合振膜单元，音质不错。单次续航7小时，配合充电盒总续航28小时。支持游戏低延迟模式，适合打游戏。"
        }
    ],
    "充电宝": [
        {
            "name": "小米移动电源3 20000mAh 快充版",
            "price": "149",
            "features": ["20000mAh大容量", "双向快充", "多设备充电", "轻薄设计", "安全保护"],
            "description": "小米移动电源3容量20000mAh，支持18W双向快充。可同时为3台设备充电，配备2个USB-A口和1个USB-C口。采用高品质锂离子聚合物电池，轻薄便携。内置多重安全保护，支持边充边放。"
        },
        {
            "name": "罗马仕 30000mAh 超大容量充电宝",
            "price": "199",
            "features": ["30000mAh容量", "22.5W快充", "四口输出", "数显屏", "飞机可带"],
            "description": "罗马仕30000mAh超大容量充电宝，适合长途旅行。支持22.5W快充，可为手机快速补电。配备3个USB-A口和1个USB-C口，可同时充4台设备。LED数显屏显示剩余电量。容量符合民航标准，可带上飞机。"
        },
        {
            "name": "Anker 20000mAh 双向快充移动电源",
            "price": "299",
            "features": ["20000mAh", "PowerIQ 3.0", "USB-C双向快充", "多协议兼容", "优质做工"],
            "description": "Anker 20000mAh移动电源采用PowerIQ 3.0智能快充技术。USB-C口支持18W双向快充，可为充电宝本身快速充电。兼容PD、QC等多种快充协议。做工精良，使用寿命长。支持边充边放，带LED电量指示灯。"
        },
        {
            "name": "品胜 10000mAh 超薄充电宝",
            "price": "89",
            "features": ["10000mAh", "轻薄小巧", "双USB输出", "智能识别", "性价比高"],
            "description": "品胜10000mAh超薄充电宝，厚度仅14mm，重量轻便携带。双USB-A输出口，可同时为两台设备充电。智能识别设备，自动匹配最佳充电电流。配备4颗LED电量指示灯。性价比高，适合日常携带使用。"
        },
        {
            "name": "绿联 50000mAh 户外大容量电源",
            "price": "599",
            "features": ["50000mAh", "AC交流输出", "笔记本可充", "太阳能充电", "户外神器"],
            "description": "绿联50000mAh户外移动电源，配备220V AC交流输出插座，可为笔记本电脑供电。多个USB口和Type-C口，支持多设备同时充电。支持太阳能板充电（需另购）。LED手电筒功能，适合户外露营、应急使用。"
        }
    ],
    "键盘": [
        {
            "name": "罗技 MX Keys S",
            "price": "799",
            "features": ["无线蓝牙", "背光键盘", "多设备切换", "70天续航", "舒适打字"],
            "description": "罗技MX Keys S是高端无线办公键盘，支持蓝牙和USB接收器双模式连接。智能背光，可根据环境光自动调节。支持3台设备快速切换，跨平台使用。充电一次可用70天（关闭背光）。键帽采用球形凹面设计，打字舒适准确。"
        },
        {
            "name": "Cherry MX Board 3.0S 机械键盘",
            "price": "599",
            "features": ["Cherry轴体", "有线连接", "PBT键帽", "全键无冲", "经典设计"],
            "description": "Cherry MX Board 3.0S采用德国原厂Cherry MX轴体，手感出色。有红轴、茶轴、青轴可选。PBT双色成型键帽，耐磨不打油。全键无冲突，支持多键同时按下。经典简约设计，适合办公和游戏。带金属面板，做工扎实。"
        },
        {
            "name": "雷蛇 黑寡妇V4专业版",
            "price": "1299",
            "features": ["雷蛇绿轴", "RGB灯效", "多功能滚轮", "腕托设计", "游戏优化"],
            "description": "雷蛇黑寡妇V4专业版游戏机械键盘，采用雷蛇第三代机械轴。Chroma RGB幻彩灯效，支持1680万色。配备多功能数字滚轮和8个专用宏按键。人体工学腕托，长时间游戏不累。支持板载内存存储配置。"
        }
    ]
}

def generate_documents():
    """生成测试文档"""
    doc_count = 0

    for category, items in products.items():
        for product in items:
            doc_count += 1
            filename = f"{doc_count:02d}_{product['name'].replace(' ', '_')}.txt"
            filepath = os.path.join(output_dir, filename)

            # 生成文档内容
            content = f"""商品名称：{product['name']}

分类：{category}

价格：¥{product['price']}

主要特点：
"""
            for i, feature in enumerate(product['features'], 1):
                content += f"{i}. {feature}\n"

            content += f"""
详细介绍：
{product['description']}

适用人群：
"""
            if category == "手机":
                content += """- 追求性能的用户
- 喜欢拍照的用户
- 商务办公人士
- 科技爱好者"""
            elif category == "耳机":
                content += """- 通勤上班族
- 音乐爱好者
- 需要降噪的用户
- 运动健身人士"""
            elif category == "充电宝":
                content += """- 经常外出的用户
- 商务出差人士
- 旅行爱好者
- 手机重度使用者"""
            elif category == "键盘":
                content += """- 程序员
- 办公室白领
- 游戏玩家
- 打字员"""

            content += f"""

购买建议：
{product['name']} 是{category}类别中的{['优质', '热门', '高性价比', '旗舰'][random.randint(0, 3)]}选择。"""

            if int(product['price']) > 1000:
                content += "适合预算充足、追求品质的用户。"
            elif int(product['price']) > 500:
                content += "性能与价格平衡，适合大多数用户。"
            else:
                content += "价格实惠，性价比高，适合预算有限的用户。"

            content += f"""

售后服务：
- 全国联保
- 7天无理由退货
- 质量问题免费换货
- 官方客服支持

注意事项：
- 请从正规渠道购买
- 注意查验商品包装
- 保留购买凭证
- 如有问题及时联系售后

最后更新时间：2024年1月"""

            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ 已生成: {filename}")

    print(f"\n🎉 总共生成 {doc_count} 个测试文档")
    print(f"📁 文档保存在: {os.path.abspath(output_dir)}")
    print("\n下一步：")
    print("1. 启动前端：访问 http://localhost:5173")
    print("2. 登录管理员账号：admin / 123456")
    print("3. 进入知识库管理页面")
    print(f"4. 上传 {output_dir} 目录下的文档")

if __name__ == "__main__":
    print("=" * 60)
    print("生成测试知识库文档")
    print("=" * 60)
    print()
    generate_documents()
