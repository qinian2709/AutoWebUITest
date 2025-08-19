"""
TeacherIn网站测试用例 - PO设计模式
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.teacherin_page import TeacherInHomePage, TeacherInEducationPage
from utils.test_case_base import TestCaseBase
from utils.decorators import step_screenshot
from utils.logger import log

@allure.epic("TeacherIn网站")
@allure.feature("页面解耦与多页面对象组合")
class TestTeacherInNavigation(TestCaseBase):
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.setup_test_environment(page)
        urls = self.get_urls()
        
        # 获取teacherin_user_page场景的数据
        teacherin_data = self.get_test_data().get_all_data().get("teacherin_user_page", {})
        selectors_data = teacherin_data.get("selectors", {})
        target_data = teacherin_data.get("target", {})
        
        # 初始化页面对象
        self.home_page = TeacherInHomePage(page, base_url=urls["teacherin_user_page"], selectors=selectors_data, target_data=target_data)
        self.education_page = TeacherInEducationPage(page, selectors=selectors_data, target_data=target_data)
        
        # 存储断言数据
        self.target_data = target_data
        
        self.log_test_data("teacherin_user_page")

    @allure.story("分页面对象组合操作")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @pytest.mark.smoke
    def test_teacherin_multi_page(self, page: Page):
        # 步骤1: 首页操作
        self._step_open_homepage(page)
        # 步骤2: 校外教育页面操作
        self._step_click_core_literacy(page)
        # 步骤3: 通用断言
        self._step_verify_url(page)


    # ~~~~~~~~~~~~~~~~~~~~~~私有方法~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @step_screenshot("打开个人主页-验证主页元素") #截图装饰器，如不需要可不添加
    def _step_open_homepage(self, page: Page):
        assert self.home_page.open_homepage(), "打开个人主页失败"
        # 使用页面对象的验证方法
        assert self.home_page.verify_homepage_elements(), "主页元素校验失败"
        assert self.home_page.click_star_course(), "点击收藏的课程失败"
        
        

    @step_screenshot("主页点击发布课程-验证发布课程")
    def _step_click_core_literacy(self, page: Page):
        assert self.education_page.click_post_course(), "点击发布的课程失败"
        # 使用页面对象的验证方法
        assert self.education_page.verify_post_course_page(), "验证课程存在失败"


    @step_screenshot("验证URL")
    def _step_verify_url(self, page: Page):
        current_url = self.education_page.get_current_url()
        log.info(f"当前页面URL: {current_url}")
        # 使用target数据中的url_contains进行验证
        expected_url_text = self.target_data.get("url_contains", "teacherin")
        assert expected_url_text in current_url, f"URL不包含{expected_url_text}"
    
    
 