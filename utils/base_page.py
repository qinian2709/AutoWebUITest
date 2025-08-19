"""
基础页面类
"""
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
from utils.logger import log
from utils.wait import Wait
from utils.screenshot import Screenshot

class BasePage:
    """基础页面类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.wait = Wait(page)
        self.screenshot = Screenshot()
    
    def navigate_to(self, url: str) -> bool:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
            
        Returns:
            是否成功
        """
        try:
            log.info(f"导航到: {url}")
            self.page.goto(url)
            self.wait.wait_for_page_load()
            return True
        except Exception as e:
            log.error(f"导航失败: {url}, 错误: {str(e)}")
            return False
    
    def click(self, selector: str, timeout: int = 10000) -> bool:
        """
        点击元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            是否成功
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                element.click()
                log.info(f"点击元素: {selector}")
                return True
            return False
        except Exception as e:
            log.error(f"点击元素失败: {selector}, 错误: {str(e)}")
            return False
    
    def type_text(self, selector: str, text: str, timeout: int = 10000) -> bool:
        """
        输入文本
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
            timeout: 超时时间
            
        Returns:
            是否成功
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                element.fill(text)
                log.info(f"输入文本: {text} 到 {selector}")
                return True
            return False
        except Exception as e:
            log.error(f"输入文本失败: {selector}, 错误: {str(e)}")
            return False
    
    def get_text(self, selector: str, timeout: int = 10000) -> Optional[str]:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            元素文本
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                text = element.text_content()
                log.info(f"获取文本: {text} 从 {selector}")
                return text
            return None
        except Exception as e:
            log.error(f"获取文本失败: {selector}, 错误: {str(e)}")
            return None
    
    def get_attribute(self, selector: str, attribute: str, timeout: int = 10000) -> Optional[str]:
        """
        获取元素属性
        
        Args:
            selector: 元素选择器
            attribute: 属性名
            timeout: 超时时间
            
        Returns:
            属性值
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                value = element.get_attribute(attribute)
                log.info(f"获取属性: {attribute}={value} 从 {selector}")
                return value
            return None
        except Exception as e:
            log.error(f"获取属性失败: {selector}, 错误: {str(e)}")
            return None
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            是否可见
        """
        try:
            element = self.page.locator(selector)
            return element.is_visible(timeout=timeout)
        except Exception as e:
            log.error(f"检查元素可见性失败: {selector}, 错误: {str(e)}")
            return False
    
    def is_element_enabled(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查元素是否启用
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            是否启用
        """
        try:
            element = self.page.locator(selector)
            return element.is_enabled(timeout=timeout)
        except Exception as e:
            log.error(f"检查元素启用状态失败: {selector}, 错误: {str(e)}")
            return False
    
    def select_option(self, selector: str, value: str, timeout: int = 10000) -> bool:
        """
        选择下拉框选项
        
        Args:
            selector: 下拉框选择器
            value: 选项值
            timeout: 超时时间
            
        Returns:
            是否成功
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                element.select_option(value=value)
                log.info(f"选择选项: {value} 从 {selector}")
                return True
            return False
        except Exception as e:
            log.error(f"选择选项失败: {selector}, 错误: {str(e)}")
            return False
    
    def hover(self, selector: str, timeout: int = 10000) -> bool:
        """
        鼠标悬停
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            是否成功
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                element.hover()
                log.info(f"鼠标悬停: {selector}")
                return True
            return False
        except Exception as e:
            log.error(f"鼠标悬停失败: {selector}, 错误: {str(e)}")
            return False
    
    def scroll_to_element(self, selector: str, timeout: int = 10000) -> bool:
        """
        滚动到元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
            
        Returns:
            是否成功
        """
        try:
            element = self.wait.wait_for_element(selector, timeout)
            if element:
                element.scroll_into_view_if_needed()
                log.info(f"滚动到元素: {selector}")
                return True
            return False
        except Exception as e:
            log.error(f"滚动到元素失败: {selector}, 错误: {str(e)}")
            return False
    
    def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.page.title()
    
    def get_current_url(self) -> str:
        """
        获取当前URL
        
        Returns:
            当前URL
        """
        return self.page.url
    
    def refresh_page(self) -> bool:
        """
        刷新页面
        
        Returns:
            是否成功
        """
        try:
            self.page.reload()
            self.wait.wait_for_page_load()
            log.info("页面已刷新")
            return True
        except Exception as e:
            log.error(f"刷新页面失败: {str(e)}")
            return False
    
    def go_back(self) -> bool:
        """
        返回上一页
        
        Returns:
            是否成功
        """
        try:
            self.page.go_back()
            self.wait.wait_for_page_load()
            log.info("已返回上一页")
            return True
        except Exception as e:
            log.error(f"返回上一页失败: {str(e)}")
            return False
    
    def go_forward(self) -> bool:
        """
        前进到下一页
        
        Returns:
            是否成功
        """
        try:
            self.page.go_forward()
            self.wait.wait_for_page_load()
            log.info("已前进到下一页")
            return True
        except Exception as e:
            log.error(f"前进到下一页失败: {str(e)}")
            return False 