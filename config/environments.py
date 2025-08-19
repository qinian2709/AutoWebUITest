"""
环境管理器 - 简化版，只负责环境标识和路径管理
"""
import os

class EnvironmentManager:
    """环境管理器 - 简化版"""
    
    @classmethod
    def get_current_env(cls) -> str:
        """获取当前环境"""
        return os.getenv("ENV", "test")
    
    @classmethod
    def get_test_data_path(cls, env: str = None) -> str:
        """获取测试数据路径"""
        if env is None:
            env = cls.get_current_env()
        return f"data/{env}"
    
    @classmethod
    def get_report_path(cls, env: str = None) -> str:
        """获取报告路径"""
        if env is None:
            env = cls.get_current_env()
        return f"reports/{env}" 