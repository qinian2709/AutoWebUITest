"""
Pytest配置文件
"""
import pytest
from playwright.sync_api import Page
from config.config import Config
from utils.screenshot import Screenshot
from utils.video_manager import VideoManager
from utils.logger import log

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """浏览器上下文参数"""
    import os
    from config.environments import EnvironmentManager
    
    # 获取当前环境
    current_env = EnvironmentManager.get_current_env()
    
    # 按环境设置视频录制路径
    videos_dir = f"./reports/{current_env}/videos"
    os.makedirs(videos_dir, exist_ok=True)
    
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "ignore_https_errors": True,
        "record_video_dir": videos_dir,
        "record_video_size": {
            "width": 1920,
            "height": 1080
        },
        "locale": "zh-CN",  # 设置中文语言环境
        "extra_http_headers": {
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
    }

@pytest.fixture
def page(page: Page):
    """页面对象"""
    # 设置视口大小
    page.set_viewport_size({
        "width": 1920,
        "height": 1080
    })
    
    # 设置超时
    page.set_default_timeout(30000)  # 30秒
    
    yield page

def pytest_runtest_makereport(item, call):
    """测试报告钩子 - 失败时截图和视频附件"""
    if call.when == "call":
        # 获取page对象
        page = None
        for fixture_name in item.funcargs:
            if fixture_name == "page":
                page = item.funcargs[fixture_name]
                break
        
        if page:
            # 初始化视频管理器
            video_manager = VideoManager()
            
            # 处理视频附件
            try:
                # 附加视频到Allure报告
                video_manager.attach_video_to_allure(page, item.name)
                
                # 保存视频文件（可选）
                # video_manager.save_video_with_test_name(page, item.name)
                
            except Exception as e:
                log.warning(f"处理视频附件失败: {e}")
            
            # 失败时额外截图（作为测试级别的失败截图）
            # if call.excinfo:
            #     screenshot = Screenshot()
            #     screenshot_path = screenshot.take_screenshot_on_failure(page, item.name)
                
            #     if screenshot_path:
            #         # 附加到Allure报告
            #         allure.attach.file(
            #             screenshot_path,
            #             name="测试失败截图",
            #             attachment_type=allure.attachment_type.PNG
            #         )
            #         log.error(f"测试失败，额外截图已保存: {screenshot_path}") 