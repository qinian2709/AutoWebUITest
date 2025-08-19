"""
基础页面类 - PO设计模式
"""
import allure
from playwright.sync_api import Page
from utils.logger import log
from utils.decorators import allure_step


class BasePage:
    """基础页面类"""
    
    def __init__(self, page: Page, base_url: str = None):
        self.page = page
        self.base_url = base_url
    
    @allure_step("导航到页面")
    def navigate_to(self, url: str = None) -> bool:
        """导航到指定页面"""
        try:
            target_url = url or self.base_url
            if not target_url:
                log.error("未提供URL")
                return False
            
            log.info(f"导航到页面: {target_url}")
            self.page.goto(target_url)
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            log.error(f"导航失败: {e}")
            return False
    
    @allure_step("点击元素")
    def click(self, selector: str, timeout: int = 10000) -> bool:
        """点击元素"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector)
            log.info(f"点击元素成功: {selector}")
            return True
        except Exception as e:
            log.error(f"点击元素失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("输入文本")
    def type_text(self, selector: str, text: str, timeout: int = 10000) -> bool:
        """输入文本"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.fill(selector, text)
            log.info(f"输入文本成功: {selector} = {text}")
            return True
        except Exception as e:
            log.error(f"输入文本失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("获取元素文本")
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """获取元素文本"""
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)
            text = element.text_content()
            log.info(f"获取文本成功: {selector} = {text}")
            return text
        except Exception as e:
            log.error(f"获取文本失败: {selector}, 错误: {e}")
            return ""
    
    @allure_step("等待元素出现")
    def wait_for_element(self, selector: str, timeout: int = 10000) -> bool:
        """等待元素出现"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            log.info(f"元素出现: {selector}")
            return True
        except Exception as e:
            log.error(f"元素未出现: {selector}, 错误: {e}")
            return False
    
    @allure_step("验证页面标题")
    def verify_title(self, expected_title: str) -> bool:
        """验证页面标题"""
        try:
            actual_title = self.page.title()
            assert expected_title in actual_title, f"页面标题不匹配，期望: {expected_title}，实际: {actual_title}"
            log.info(f"页面标题验证成功: {actual_title}")
            return True
        except Exception as e:
            log.error(f"页面标题验证失败: {e}")
            return False
    
    @allure_step("获取页面标题")
    def get_title(self) -> str:
        """获取页面标题"""
        return self.page.title()
    
    @allure_step("检查元素可见性")
    def is_element_visible(self, selector: str, timeout: int = 10000) -> bool:
        """检查元素是否可见"""
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)
            return element.is_visible()
        except Exception as e:
            log.error(f"检查元素可见性失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("等待页面加载")
    def wait_for_page_load(self, timeout: int = 30000) -> bool:
        """等待页面完全加载"""
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception as e:
            log.error(f"等待页面加载失败: {e}")
            return False
    
    @allure_step("获取当前URL")
    def get_current_url(self) -> str:
        """获取当前页面URL"""
        return self.page.url
    
    @allure_step("验证URL包含")
    def verify_url_contains(self, expected_text: str) -> bool:
        """验证URL包含指定文本"""
        try:
            current_url = self.page.url
            assert expected_text in current_url, f"URL不包含期望文本，期望: {expected_text}，实际: {current_url}"
            log.info(f"URL验证成功: {current_url}")
            return True
        except Exception as e:
            log.error(f"URL验证失败: {e}")
            return False
    
    @allure_step("等待并点击元素")
    def wait_and_click(self, selector: str, timeout: int = 10000) -> bool:
        """等待元素出现并点击"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector)
            log.info(f"等待并点击元素成功: {selector}")
            return True
        except Exception as e:
            log.error(f"等待并点击元素失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("等待并输入文本")
    def wait_and_type(self, selector: str, text: str, timeout: int = 10000) -> bool:
        """等待元素出现并输入文本"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.fill(selector, text)
            log.info(f"等待并输入文本成功: {selector} = {text}")
            return True
        except Exception as e:
            log.error(f"等待并输入文本失败: {selector}, 错误: {e}")
            return False
    
    # 新增的通用方法
    @allure_step("点击文本元素")
    def click_text_element(self, text: str, element_type: str = "span", timeout: int = 10000) -> bool:
        """点击包含指定文本的元素"""
        try:
            selector = f"//{element_type}[contains(text(), '{text}') or contains(., '{text}')]"
            return self.wait_and_click(selector, timeout)
        except Exception as e:
            log.error(f"点击文本元素失败: {text}, 错误: {e}")
            return False
    
    @allure_step("验证元素存在")
    def verify_element_exists(self, selector: str, timeout: int = 10000) -> bool:
        """验证元素存在"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            log.info(f"元素存在验证成功: {selector}")
            return True
        except Exception as e:
            log.error(f"元素存在验证失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("验证文本元素存在")
    def verify_text_element_exists(self, text: str, element_type: str = "span", timeout: int = 10000) -> bool:
        """验证包含指定文本的元素存在"""
        try:
            selector = f"//{element_type}[contains(text(), '{text}') or contains(., '{text}')]"
            return self.verify_element_exists(selector, timeout)
        except Exception as e:
            log.error(f"验证文本元素存在失败: {text}, 错误: {e}")
            return False
    
    @allure_step("验证页面内容包含")
    def verify_page_content_contains(self, expected_text: str) -> bool:
        """验证页面内容包含指定文本"""
        try:
            page_content = self.page.content()
            assert expected_text in page_content, f"页面内容不包含期望文本: {expected_text}"
            log.info(f"页面内容验证成功: {expected_text}")
            return True
        except Exception as e:
            log.error(f"页面内容验证失败: {e}")
            return False
    
    @allure_step("验证页面标题包含")
    def verify_title_contains(self, expected_text: str) -> bool:
        """验证页面标题包含指定文本"""
        try:
            actual_title = self.page.title()
            assert expected_text.lower() in actual_title.lower(), f"页面标题不包含期望文本，期望: {expected_text}，实际: {actual_title}"
            log.info(f"页面标题验证成功: {actual_title}")
            return True
        except Exception as e:
            log.error(f"页面标题验证失败: {e}")
            return False
    
    @allure_step("点击并验证")
    def click_and_verify(self, selector: str, verification_method: str = None, verification_data: str = None, timeout: int = 10000) -> bool:
        """点击元素并进行验证"""
        try:
            # 点击元素
            if not self.wait_and_click(selector, timeout):
                return False
            
            # 根据验证方法进行验证
            if verification_method == "url_contains" and verification_data:
                return self.verify_url_contains(verification_data)
            elif verification_method == "title_contains" and verification_data:
                return self.verify_title_contains(verification_data)
            elif verification_method == "content_contains" and verification_data:
                return self.verify_page_content_contains(verification_data)
            else:
                log.info("点击成功，无需额外验证")
                return True
        except Exception as e:
            log.error(f"点击并验证失败: {selector}, 错误: {e}")
            return False
    
    @allure_step("点击文本元素并验证")
    def click_text_and_verify(self, text: str, element_type: str = "span", verification_method: str = None, verification_data: str = None, timeout: int = 10000) -> bool:
        """点击文本元素并进行验证"""
        try:
            selector = f"//{element_type}[contains(text(), '{text}') or contains(., '{text}')]"
            return self.click_and_verify(selector, verification_method, verification_data, timeout)
        except Exception as e:
            log.error(f"点击文本元素并验证失败: {text}, 错误: {e}")
            return False 