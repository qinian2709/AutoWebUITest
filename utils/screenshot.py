"""
截图工具类 - 支持每个步骤截图
"""
import os
from datetime import datetime
from playwright.sync_api import Page
from utils.logger import log_screenshot, log_error

class Screenshot:
    """截图工具类"""
    
    def __init__(self):
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self):
        """确保截图目录存在"""
        screenshot_dir = "./reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, page: Page, name: str = None, full_page: bool = True) -> str:
        """
        截图
        
        Args:
            page: Playwright页面对象
            name: 截图文件名
            full_page: 是否截取完整页面
            
        Returns:
            截图文件路径
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"
        
        # 确保文件名有.png后缀
        if not name.endswith('.png'):
            name += '.png'
        
        screenshot_dir = "./reports/screenshots"
        file_path = os.path.join(screenshot_dir, name)
        
        try:
            page.screenshot(path=file_path, full_page=full_page)
            log_screenshot(file_path)
            return file_path
        except Exception as e:
            log_error(f"截图失败: {str(e)}")
            return None
    
    def take_step_screenshot(self, page: Page, step_name: str, test_name: str = None) -> str:
        """
        步骤截图
        
        Args:
            page: Playwright页面对象
            step_name: 步骤名称
            test_name: 测试名称
            
        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if test_name:
            name = f"{test_name}_{step_name}_{timestamp}.png"
        else:
            name = f"step_{step_name}_{timestamp}.png"
        
        return self.take_screenshot(page, name)
    
    def take_screenshot_on_failure(self, page: Page, test_name: str) -> str:
        """
        测试失败时截图
        
        Args:
            page: Playwright页面对象
            test_name: 测试名称
            
        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"failure_{test_name}_{timestamp}.png"
        return self.take_screenshot(page, name)
    
    def take_element_screenshot(self, page: Page, selector: str, name: str = None) -> str:
        """
        元素截图
        
        Args:
            page: Playwright页面对象
            selector: 元素选择器
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"element_{timestamp}.png"
        
        if not name.endswith('.png'):
            name += '.png'
        
        screenshot_dir = "./reports/screenshots"
        file_path = os.path.join(screenshot_dir, name)
        
        try:
            element = page.locator(selector)
            element.screenshot(path=file_path)
            log_screenshot(file_path)
            return file_path
        except Exception as e:
            log_error(f"元素截图失败: {str(e)}")
            return None 