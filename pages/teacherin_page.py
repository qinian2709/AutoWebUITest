"""
TeacherIn首页页面对象 - PO设计模式
"""
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import log
from utils.decorators import allure_step

"""
TeacherIn个人主页页面对象 - PO设计模式
"""
class TeacherInHomePage(BasePage):
    def __init__(self, page: Page, base_url: str, selectors: dict, target_data: dict = None):
        super().__init__(page, base_url)
        self.star_course_text = selectors["star_course"]
        self.target_data = target_data or {}
        log.info(f"初始化TeacherIn个人主页，URL: {base_url}")

    @allure_step("打开TeacherIn个人主页")
    def open_homepage(self) -> bool:
        return self.navigate_to()

    @allure_step("点击收藏的课程")
    def click_star_course(self) -> bool:
        """使用通用方法点击文本元素"""
        return self.click_text_element(self.star_course_text)

    @allure_step("验证主页元素")
    def verify_homepage_elements(self) -> bool:
        """使用通用方法验证页面标题"""
        expected_title = self.target_data.get("homepage_title", "TeacherIn")
        return self.verify_title_contains(expected_title)

    @allure_step("验证首页标题")
    def verify_title_contains(self, expected_title: str) -> bool:
        """验证首页标题包含指定文本"""
        return super().verify_title_contains(expected_title)

"""
TeacherIn个人主页点击发布的课程 - PO设计模式
"""
class TeacherInEducationPage(BasePage):
    def __init__(self, page: Page, selectors: dict, target_data: dict = None):
        super().__init__(page)
        self.post_course_text = selectors["post_course"]
        self.target_data = target_data or {}
        log.info("无需初始化页面，直接点击发布的课程")

    @allure_step("点击发布的课程")
    def click_post_course(self) -> bool:
        """使用通用方法点击文本元素"""
        return self.click_text_element(self.post_course_text)

    @allure_step("验证个人主页")
    def verify_post_course_page(self) -> bool:
        """使用通用方法验证页面内容"""
        expected_content = self.target_data.get("core_literacy_content", self.post_course_text)
        return self.verify_page_content_contains(expected_content)

    @allure_step("验证页面内容包含")
    def verify_page_content_contains(self, expected_content: str) -> bool:
        """验证页面内容包含指定文本"""
        return super().verify_page_content_contains(expected_content) 