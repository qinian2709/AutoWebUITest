"""
等待工具类
"""
import time
from typing import Optional, Callable
from playwright.sync_api import Page, Locator, expect
from utils.logger import log

class Wait:
    """等待工具类"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def wait_for_element(self, selector: str, timeout: int = 10000) -> Optional[Locator]:
        """
        等待元素出现
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            元素定位器
        """
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            log.info(f"元素已出现: {selector}")
            return element
        except Exception as e:
            log.error(f"等待元素超时: {selector}, 错误: {str(e)}")
            return None
    
    def wait_for_element_disappear(self, selector: str, timeout: int = 10000) -> bool:
        """
        等待元素消失
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            是否消失
        """
        try:
            element = self.page.locator(selector)
            element.wait_for(state="hidden", timeout=timeout)
            log.info(f"元素已消失: {selector}")
            return True
        except Exception as e:
            log.error(f"等待元素消失超时: {selector}, 错误: {str(e)}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30000) -> bool:
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            是否加载完成
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            log.info("页面加载完成")
            return True
        except Exception as e:
            log.error(f"页面加载超时: {str(e)}")
            return False
    
    def wait_for_url(self, url: str, timeout: int = 10000) -> bool:
        """
        等待URL变化
        
        Args:
            url: 期望的URL
            timeout: 超时时间(毫秒)
            
        Returns:
            是否匹配
        """
        try:
            self.page.wait_for_url(url, timeout=timeout)
            log.info(f"URL已匹配: {url}")
            return True
        except Exception as e:
            log.error(f"等待URL超时: {url}, 错误: {str(e)}")
            return False
    
    def wait_for_condition(self, condition: Callable, timeout: int = 10000, interval: float = 0.5) -> bool:
        """
        等待自定义条件
        
        Args:
            condition: 条件函数
            timeout: 超时时间(毫秒)
            interval: 检查间隔(秒)
            
        Returns:
            条件是否满足
        """
        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            try:
                if condition():
                    log.info("自定义条件已满足")
                    return True
            except Exception as e:
                log.debug(f"检查条件时出错: {str(e)}")
            
            time.sleep(interval)
        
        log.error(f"等待自定义条件超时: {timeout}ms")
        return False
    
    def wait_for_text(self, text: str, timeout: int = 10000) -> bool:
        """
        等待文本出现
        
        Args:
            text: 期望的文本
            timeout: 超时时间(毫秒)
            
        Returns:
            是否出现
        """
        try:
            self.page.wait_for_selector(f"text={text}", timeout=timeout)
            log.info(f"文本已出现: {text}")
            return True
        except Exception as e:
            log.error(f"等待文本超时: {text}, 错误: {str(e)}")
            return False
    
    def wait_for_network_idle(self, timeout: int = 10000) -> bool:
        """
        等待网络空闲
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            是否空闲
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            log.info("网络已空闲")
            return True
        except Exception as e:
            log.error(f"等待网络空闲超时: {str(e)}")
            return False 