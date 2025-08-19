"""
日志工具类 - 美化输出格式
"""
import os
import sys
from datetime import datetime
from loguru import logger

class Logger:
    """日志管理类"""
    
    def __init__(self):
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 移除默认的日志处理器
        logger.remove()
        
        # 创建日志目录
        log_dir = "./reports/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 美化控制台日志格式
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        # 文件日志格式（保持简洁）
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )
        
        # 添加控制台处理器
        logger.add(
            sys.stdout,
            format=console_format,
            level="INFO",
            colorize=True
        )
        
        # 添加文件处理器
        log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logger.add(
            log_file,
            format=file_format,
            level="INFO",
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
    
    def get_logger(self):
        """获取logger实例"""
        return logger
    
    def info(self, message: str):
        """信息日志"""
        logger.info(message)
    
    def debug(self, message: str):
        """调试日志"""
        logger.debug(message)
    
    def warning(self, message: str):
        """警告日志"""
        logger.warning(message)
    
    def error(self, message: str):
        """错误日志"""
        logger.error(message)
    
    def critical(self, message: str):
        """严重错误日志"""
        logger.critical(message)

# 全局日志实例
log = Logger().get_logger()

# 美化日志输出函数
def log_step(step_name: str, status: str = "开始", details: str = ""):
    """记录测试步骤"""
    icons = {
        "开始": "🚀",
        "成功": "✅", 
        "失败": "❌",
        "跳过": "⏭️",
        "警告": "⚠️",
        "信息": "ℹ️"
    }
    
    icon = icons.get(status, "📝")
    color = {
        "开始": "blue",
        "成功": "green",
        "失败": "red", 
        "跳过": "yellow",
        "警告": "yellow",
        "信息": "cyan"
    }.get(status, "white")
    
    message = f"{icon} {step_name} - {status}"
    if details:
        message += f" | {details}"
    
    log.info(message)

def log_test_data(data_type: str, data: dict):
    """记录测试数据"""
    log.info(f"📊 {data_type}:")
    for key, value in data.items():
        if isinstance(value, dict):
            log.info(f"   📁 {key}:")
            for sub_key, sub_value in value.items():
                log.info(f"      • {sub_key}: {sub_value}")
        else:
            log.info(f"   • {key}: {value}")

def log_page_action(action: str, element: str = "", result: str = ""):
    """记录页面操作"""
    icon = "🖱️" if "点击" in action else "🔍" if "验证" in action else "📄"
    message = f"{icon} {action}"
    if element:
        message += f" | 元素: {element}"
    if result:
        message += f" | 结果: {result}"
    log.info(message)

def log_screenshot(filename: str):
    """记录截图"""
    log.info(f"📸 截图已保存: {filename}")

def log_video(filename: str):
    """记录视频"""
    log.info(f"🎥 视频已保存: {filename}")

def log_url(url: str):
    """记录URL"""
    log.info(f"🌐 当前页面: {url}")

def log_warning(message: str):
    """记录警告"""
    log.warning(f"⚠️ {message}")

def log_error(message: str):
    """记录错误"""
    log.error(f"❌ {message}")

def log_success(message: str):
    """记录成功"""
    log.info(f"✅ {message}")

def log_info(message: str):
    """记录信息"""
    log.info(f"ℹ️ {message}")

def log_debug(message: str):
    """记录调试信息"""
    log.debug(f"🔍 {message}") 