"""
Playwright配置文件
"""
from playwright.sync_api import Playwright, sync_playwright, expect
import os
from config.config import Config

def run(playwright: Playwright) -> None:
    """运行配置"""
    config = Config()
    
    # 获取浏览器类型，默认为 chromium
    browser_type = os.getenv("BROWSER", "chromium")
    
    # 启动浏览器
    if browser_type == "chromium":
        browser = playwright.chromium.launch(
            headless=config.HEADLESS,
            slow_mo=0
        )
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(
            headless=config.HEADLESS,
            slow_mo=0
        )
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(
            headless=config.HEADLESS,
            slow_mo=0
        )
    else:
        browser = playwright.chromium.launch(
            headless=config.HEADLESS,
            slow_mo=0
        )
    
    # 创建上下文
    context = browser.new_context(
        viewport={
            "width": 1920,
            "height": 1080
        },
        locale="zh-CN",  # 设置中文语言环境
        extra_http_headers={
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        },
        record_video_dir="./reports/videos" if not config.HEADLESS else None,
        record_video_size={"width": 1920, "height": 1080}
    )
    
    # 创建页面
    page = context.new_page()
    
    # 设置超时
    page.set_default_timeout(config.TIMEOUT * 1000)
    
    return browser, context, page

def get_browser_context_page():
    """获取浏览器、上下文和页面实例"""
    with sync_playwright() as playwright:
        return run(playwright)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser, context, page = run(playwright)
        try:
            # 测试代码
            page.goto("https://example.com")
            print(f"页面标题: {page.title()}")
        finally:
            context.close()
            browser.close() 