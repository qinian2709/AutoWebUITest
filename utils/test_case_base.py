"""
测试用例基类 - 提供环境初始化和公共方法
"""
import pytest
import allure
from typing import Optional, Dict, Any, List
from playwright.sync_api import Page
from config.environments import EnvironmentManager
from utils.test_data_manager import TestDataManager
from utils.decorators import allure_step
from utils.logger import log


class TestCaseBase:
    """测试用例基类 - 提供公共方法和工具"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置 - 由子类实现"""
        pass
    
    def setup_test_environment(self, page: Page, page_class=None, env: str = None):
        """
        设置测试环境
        
        Args:
            page: Playwright页面对象
            page_class: 页面类，如果为None则不初始化页面对象
            env: 环境名称，如果为None则使用当前环境
        """    
        from config.config import config
        
        # 获取当前环境
        current_env = env or EnvironmentManager.get_current_env()
        
        # 初始化测试数据管理器
        self.test_data_manager = TestDataManager(env=current_env)
        
        # 初始化页面对象（如果提供了页面类）
        if page_class:
            self.page_object = page_class(page, env=current_env)
        
        # 记录环境信息
        log.info(f"测试环境: {self.test_data_manager.current_env}")
        log.info(f"测试数据路径: {self.test_data_manager.data_path}")
        
        return self.get_env_config()
    
    def setup_page_object(self, page: Page, page_class, env: str = None):
        """设置页面对象"""
        self.setup_test_environment(page, page_class, env)
        self.page_object = self.page_object
    
    def get_test_data(self):
        """获取测试数据管理器"""
        return self.test_data_manager
    
    def get_env_config(self):
        """获取环境配置"""
        return {
            'name': self.test_data_manager.current_env,
        }
    
    def get_env_data(self) -> Dict[str, Any]:
        """获取环境数据"""
        return {
            'config': self.get_env_config(),
            'test_data': self.get_test_data()
        }
    
    
    def get_urls(self) -> Dict[str, str]:
        """获取URL配置"""
        return self.test_data_manager.get_urls()
    
    def get_timeouts(self) -> Dict[str, int]:
        """获取超时配置"""
        return self.test_data_manager.get_timeouts()
    
    @allure_step("记录测试数据")
    def log_test_data(self, page_name: str = None):
        """
        记录测试数据到Allure报告
        
        Args:
            page_name: 页面名称，如果指定则只打印该页面的相关数据
        """
        env_data = self.get_env_data()
        
        if page_name:
            # 只打印指定页面的数据
            page_data = self.get_test_data().get_all_data().get(page_name, {})
            
            # 构建过滤后的数据
            filtered_data = {
                'config': env_data['config'],
                'page_data': {
                    page_name: page_data
                },
                'urls': {k: v for k, v in self.get_urls().items() if page_name in k or k == page_name},
                'timeouts': self.get_timeouts()
            }
            
            allure.attach(
                str(filtered_data),
                name=f"测试环境数据 - {page_name}",
                attachment_type=allure.attachment_type.TEXT
            )
            
            log.info(f"测试环境: {self.test_data_manager.current_env}")
            log.info(f"页面数据 - {page_name}: {page_data}")
            log.info(f"相关URL配置: {filtered_data['urls']}")
            log.info(f"超时配置: {self.get_timeouts()}")
        else:
            # 打印所有数据（原有逻辑）
            allure.attach(
                str(env_data),
                name="测试环境数据",
                attachment_type=allure.attachment_type.TEXT
            )
            
            log.info(f"测试环境: {self.test_data_manager.current_env}")
            log.info(f"URL配置: {self.get_urls()}")
            log.info(f"超时配置: {self.get_timeouts()}")
    
    def skip_if_no_data(self, data_name: str, data_list: list):
        """如果没有数据则跳过测试"""
        if not data_list:
            pytest.skip(f"跳过测试：{data_name} 数据为空")
    
    def skip_if_condition(self, condition: bool, reason: str):
        """如果满足条件则跳过测试"""
        if condition:
            pytest.skip(f"跳过测试：{reason}") 