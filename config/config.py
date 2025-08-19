"""
配置管理模块 - 统一管理框架配置
"""
import os
from typing import Dict, Any
from config.environments import EnvironmentManager
from utils.test_data_manager import TestDataManager

class Config:
    """配置类"""
    def __init__(self):
        self.env_manager = EnvironmentManager()
        # 初始化测试数据管理器
        self.test_data_manager = TestDataManager()
        # 环境配置现在直接从 EnvironmentManager 获取
        self.env_config = {"name": self.env_manager.get_current_env()}
    
    @property
    def ENV(self) -> str:
        """当前环境"""
        return self.env_manager.get_current_env()
    
    @property
    def TIMEOUT(self) -> int:
        """超时时间"""
        timeouts = self.test_data_manager.get_all_data().get("timeouts", {})
        return timeouts.get("medium", 10000)
    
    @property
    def HEADLESS(self) -> bool:
        """是否无头模式"""
        return True  # 默认使用无头模式
    
    @property
    def TEST_DATA_PATH(self) -> str:
        """测试数据路径"""
        return self.env_manager.get_test_data_path()
    
    @property
    def REPORT_PATH(self) -> str:
        """报告路径"""
        return self.env_manager.get_report_path()
    
    @property
    def VIDEOS_PATH(self) -> str:
        """视频路径"""
        return os.path.join(self.REPORT_PATH, "videos")
    
    @property
    def SCREENSHOTS_PATH(self) -> str:
        """截图路径"""
        return os.path.join(self.REPORT_PATH, "screenshots")
    
    @property
    def LOG_PATH(self) -> str:
        """日志路径"""
        return os.path.join(self.REPORT_PATH, "logs")
    
    @property
    def ENVIRONMENT_NAME(self) -> str:
        """环境名称"""
        return self.env_manager.get_current_env()
    
    @property
    def TEST_USERS(self) -> list:
        """测试用户列表"""
        return self.test_data_manager.get_all_data().get("test_users", [])
    
    @property
    def SEARCH_KEYWORDS(self) -> list:
        """搜索关键词列表"""
        return self.test_data_manager.get_all_data().get("search_keywords", [])
    
    def get_test_user(self, index: int = 0) -> Dict[str, str]:
        """获取测试用户"""
        users = self.TEST_USERS
        if users and index < len(users):
            return users[index]
        return {"username": "", "password": ""}
    
    def get_username(self, index: int = 0) -> str:
        """获取用户名"""
        user = self.get_test_user(index)
        return user.get("username", "")
    
    def get_password(self, index: int = 0) -> str:
        """获取密码"""
        user = self.get_test_user(index)
        return user.get("password", "")
    
    def get_screenshot_path(self, filename: str) -> str:
        """获取截图文件路径"""
        return os.path.join(self.SCREENSHOTS_PATH, filename)
    
    def get_log_path(self, filename: str) -> str:
        """获取日志文件路径"""
        return os.path.join(self.LOG_PATH, filename)

# 全局配置实例
config = Config() 