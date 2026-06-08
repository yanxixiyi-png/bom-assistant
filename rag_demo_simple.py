import numpy as np

# 模拟的 BOM 知识库
bom_knowledge = [
    {"id": "001", "零件号": "M12-BOLT-001", "描述": "六角螺栓 M12x50", "材质": "不锈钢304", "单重(kg)": 0.12, "标准": "GB/T 5782-2016", "关键词": ["M12", "螺栓", "不锈钢", "5782"]},
    {"id": "002", "零件号": "NUT-M12-002", "描述": "六角螺母 M12", "材质": "不锈钢304", "单重(kg)": 0.03, "标准": "GB/T 6170-2015", "关键词": ["M12", "螺母", "不锈钢", "6170"]},
    {"id": "003", "零件号": "WSH-FLAT-003", "描述": "平垫圈 M12", "材质": "不锈钢304", "单重(kg)": 0.01, "标准": "GB/T 97.1-2002", "关键词": ["M12", "垫圈", "不锈钢", "97.1"]},
    {"id": "004", "零件号": "BRKT-LEFT-004", "描述": "左支架", "材质": "Q235钢", "单重(kg)": 1.25, "标准": "企业标准", "关键词": ["左支架", "Q235", "支架"]},
]

def search_by_keywords(query, knowledge):
    query_lower = query.lower()
    scores = []
    for item in knowledge:
        score = 0
        for kw in item["关键词"]:
            if kw.lower() in query_lower:
                score += 1
        if item["零件号"].lower() in query_lower:
            score += 2
        if item["描述"].lower() in query_lower:
            score += 1
        scores.append(score)
    ranked = sorted(zip(knowledge, scores), key=lambda x: x[1], reverse=True)
    return [item for item, score in ranked if score > 0]

print("=" * 60)
print("✅ RAG 知识库已加载，共", len(bom_knowledge), "条零件信息")
print("输入 exit 退出")
print("试试问：M12螺栓的标准是什么？")
print("=" * 60)

while True:
    query = input("\n你问：")
    if query.lower() == "exit":
        print("再见！")
        break
    results = search_by_keywords(query, bom_knowledge)
    if results:
        print("\n📦 检索结果：")
        for i, item in enumerate(results[:3], 1):
            print(f"{i}. {item['零件号']} - {item['描述']} - 材质：{item['材质']} - 标准：{item['标准']}")
    else:
        print("❌ 未找到")
