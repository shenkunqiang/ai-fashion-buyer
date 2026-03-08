#!/usr/bin/env python3
"""
定时任务：生成每日报告
"""
import json
from datetime import datetime

def generate_report():
    """生成每日报告"""
    # 读取趋势数据
    try:
        with open("/app/ai-fashion-buyer/data/trends.json", "r", encoding="utf-8") as f:
            trends = json.load(f)
    except:
        trends = []
    
    # 生成报告
    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_trends": len(trends),
        "top_trends": sorted(trends, key=lambda x: x.get("trend_score", 0), reverse=True)[:5],
        "generated_at": datetime.now().isoformat()
    }
    
    # 保存报告
    with open(f"/app/ai-fashion-buyer/data/report_{datetime.now().strftime('%Y%m%d')}.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成了每日报告: {report['date']}")
    return report

if __name__ == "__main__":
    generate_report()
