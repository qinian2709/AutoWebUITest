#!/usr/bin/env python3
"""
简化的企业微信通知脚本
用法: python send_wechat_notice.py <webhook_url> <message_content>
"""
import sys
import requests
import json
from loguru import logger


def send_wechat_notice(webhook_url, message_content):
    """
    发送企业微信通知
    
    Args:
        webhook_url: 企业微信Webhook URL
        message_content: 消息内容（Markdown格式）
        
    Returns:
        bool: 发送是否成功
    """
    try:
        # 构建请求数据
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message_content
            }
        }
        
        # 发送请求
        response = requests.post(
            webhook_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                logger.success("企业微信通知发送成功")
                return True
            else:
                logger.error(f"企业微信通知发送失败: {result.get('errmsg', '未知错误')}")
                return False
        else:
            logger.error(f"企业微信通知发送失败，HTTP状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"企业微信通知发送异常: {e}")
        return False
    except Exception as e:
        logger.error(f"企业微信通知发送失败: {e}")
        return False


def main():
    """主函数"""
    # 检查参数数量
    if len(sys.argv) != 3:
        print("用法: python send_wechat_notice.py <webhook_url> <message_content>")
        print("示例: python send_wechat_notice.py 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx' '测试消息'")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    message_content = sys.argv[2]
    
    # 发送通知
    success = send_wechat_notice(webhook_url, message_content)
    
    # 输出结果
    if success:
        print("✅ 企业微信通知发送成功")
        sys.exit(0)
    else:
        print("❌ 企业微信通知发送失败")
        sys.exit(1)


if __name__ == "__main__":
    main() 