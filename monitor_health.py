#!/usr/bin/env python3
"""
系统健康监控
"""
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json

def check_api_health():
    """检查API健康状态"""
    try:
        r = requests.get("http://localhost:8000/health", timeout=5)
        if r.status_code == 200:
            return True
    except:
        return False

def send_alert(message):
    """发送告警邮件"""
    # 简化版本 - 实际需要配置SMTP
    print(f"🚨 告警: {message}")

def main():
    print(f"[{datetime.now()}] 检查系统健康...")
    
    if check_api_health():
        print("✅ API服务正常")
    else:
        send_alert("API服务异常")
    
    # 检查磁盘空间
    import shutil
    usage = shutil.disk_usage("/")
    print(f"📊 磁盘使用: {usage.used/usage.total*100:.1f}%")

if __name__ == "__main__":
    main()
