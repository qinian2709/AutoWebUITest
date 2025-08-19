"""
测试数据管理器 - 动态加载不同环境的测试数据
"""
import json
import os
from typing import Dict, Any, List, Optional
from config.environments import EnvironmentManager

class TestDataManager:
    """测试数据管理器"""
    
    def __init__(self, env: str = None):
        """
        初始化测试数据管理器
        
        Args:
            env: 环境名称，如果为None则使用当前环境
        """
        self.env = env or EnvironmentManager.get_current_env()
        self.test_data_path = EnvironmentManager.get_test_data_path(self.env)
        self._test_data = None
        self._common_data = None
        self._load_common_data()
        self._load_test_data()
    
    def _load_common_data(self):
        """加载公共测试数据"""
        try:
            common_data_file = os.path.join("data", "common.json")
            if os.path.exists(common_data_file):
                with open(common_data_file, 'r', encoding='utf-8') as f:
                    self._common_data = json.load(f)
                print(f"✅ 成功加载公共测试数据: {common_data_file}")
            else:
                print(f"⚠️ 公共测试数据文件不存在: {common_data_file}")
                self._common_data = {}
        except Exception as e:
            print(f"❌ 加载公共测试数据失败: {str(e)}")
            self._common_data = {}
    
    def _load_test_data(self):
        """加载测试数据并解析引用"""
        try:
            test_data_file = os.path.join(self.test_data_path, "test_data.json")
            if os.path.exists(test_data_file):
                with open(test_data_file, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                
                # 解析引用并合并数据
                self._test_data = self._resolve_references(raw_data)
                
                # 从环境变量覆盖敏感数据（如果存在）
                self._override_sensitive_data_from_env()
                
                print(f"✅ 成功加载并解析 {self.env} 环境测试数据: {test_data_file}")
            else:
                print(f"⚠️ 测试数据文件不存在: {test_data_file}")
                self._test_data = {}
        except Exception as e:
            print(f"❌ 加载测试数据失败: {str(e)}")
            self._test_data = {}
    
    def _override_sensitive_data_from_env(self):
        """从环境变量覆盖敏感数据"""
        # 覆盖测试用户数据
        if os.getenv("TEST_USERNAME") and os.getenv("TEST_PASSWORD"):
            self._test_data["test_users"] = [{
                "username": os.getenv("TEST_USERNAME"),
                "password": os.getenv("TEST_PASSWORD")
            }]
        
        # 覆盖用户页面URL
        if os.getenv("TEACHERIN_USER_URL"):
            if "urls" not in self._test_data:
                self._test_data["urls"] = {}
            self._test_data["urls"]["teacherin_user_page"] = os.getenv("TEACHERIN_USER_URL")
    
    def _resolve_references(self, data: Any) -> Any:
        """
        解析数据中的引用
        
        Args:
            data: 原始数据
            
        Returns:
            解析后的数据
        """
        if isinstance(data, dict):
            resolved_data = {}
            for key, value in data.items():
                resolved_data[key] = self._resolve_references(value)
            return resolved_data
        elif isinstance(data, list):
            return [self._resolve_references(item) for item in data]
        elif isinstance(data, str) and data.startswith("${") and data.endswith("}"):
            # 解析引用格式: ${common.key1.key2}
            reference_path = data[2:-1]  # 移除 ${ 和 }
            return self._get_reference_value(reference_path)
        else:
            return data
    
    def _get_reference_value(self, reference_path: str) -> Any:
        """
        根据引用路径获取值
        
        Args:
            reference_path: 引用路径，格式如 "common.key1.key2"
            
        Returns:
            引用的值
        """
        try:
            # 解析路径
            parts = reference_path.split(".")
            if parts[0] == "common" and self._common_data:
                # 从公共数据中获取
                current = self._common_data
                for part in parts[1:]:
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        print(f"⚠️ 引用路径不存在: {reference_path}")
                        return f"${reference_path}"  # 返回原始引用
                return current
            else:
                print(f"⚠️ 不支持的引用格式: {reference_path}")
                return f"${reference_path}"  # 返回原始引用
        except Exception as e:
            print(f"❌ 解析引用失败: {reference_path}, 错误: {str(e)}")
            return f"${reference_path}"  # 返回原始引用
    
    def get_search_keywords(self) -> List[str]:
        """获取搜索关键词列表"""
        return self._test_data.get("search_keywords", [])
    
    def get_test_users(self) -> List[Dict[str, str]]:
        """获取测试用户列表"""
        return self._test_data.get("test_users", [])
    
    def get_urls(self) -> Dict[str, str]:
        """获取URL配置"""
        return self._test_data.get("urls", {})
    
    def get_timeouts(self) -> Dict[str, int]:
        """获取超时配置"""
        return self._test_data.get("timeouts", {})
    
    def get_url(self, key: str) -> Optional[str]:
        """获取指定URL"""
        urls = self.get_urls()
        return urls.get(key)
    
    def get_timeout(self, key: str) -> int:
        """获取指定超时时间"""
        timeouts = self.get_timeouts()
        return timeouts.get(key, 10000)
    
    def get_test_user(self, index: int = 0) -> Optional[Dict[str, str]]:
        """获取测试用户"""
        users = self.get_test_users()
        if 0 <= index < len(users):
            return users[index]
        return None
    
    def get_search_keyword(self, index: int = 0) -> Optional[str]:
        """获取搜索关键词"""
        keywords = self.get_search_keywords()
        if 0 <= index < len(keywords):
            return keywords[index]
        return None
    
    def get_all_data(self) -> Dict[str, Any]:
        """获取所有测试数据"""
        return self._test_data.copy()
    
    def reload_data(self):
        """重新加载测试数据"""
        self._load_common_data()
        self._load_test_data()
    
    @property
    def current_env(self) -> str:
        """获取当前环境"""
        return self.env
    
    @property
    def data_path(self) -> str:
        """获取数据路径"""
        return self.test_data_path 