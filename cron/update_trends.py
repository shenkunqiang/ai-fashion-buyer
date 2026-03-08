#!/usr/bin/env python3
"""
定时任务：更新趋势数据
从社交媒体获取最新流行趋势
"""
import sys
import json
import random
from datetime import datetime

# 模拟从外部API获取趋势数据
def fetch_trends():
    """模拟获取趋势数据"""
    sources = ["小红书", "抖音", "微博", "B站"]
    tags_pool = [
        ["职场", "通勤", "OL"], ["复古", "港风", "怀旧"],
        ["运动", "健身", "户外"], ["休闲", "舒适", "居家"],
        ["甜美", "公主", "洛丽塔"], ["街头", "嘻哈", "潮牌"],
        ["极简", "北欧", "冷淡"], ["国风", "新中式", "汉元素"]
    ]
    
    trends = []
    for i in range(10):
        trends.append({
            "title": f"第{i+1}个流行趋势",
            "source": random.choice(sources),
            "tags": random.choice(tags_pool),
            "likes": random.randint(1000, 50000),
            "trend_score": round(random.uniform(7.0, 9.9), 1),
            "updated_at": datetime.now().isoformat()
        })
    
    # 保存到文件
    with open("/app/ai-fashion-buyer/data/trends.json", "w", encoding="utf-8") as f:
        json.dump(trends, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新了 {len(trends)} 条趋势数据")
    return trends

if __name__ == "__main__":
    fetch_trends()
