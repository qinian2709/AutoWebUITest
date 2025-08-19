"""
装饰器工具模块
"""
import functools
import allure
from typing import Optional, Callable, Any
from playwright.sync_api import Page
from utils.screenshot import Screenshot
from utils.video_manager import VideoManager
from utils.logger import log


def step_screenshot(step_name: str = None, attach_to_allure: bool = True):
    """
    截图装饰器 - 自动为测试步骤添加截图（成功失败都截图）
    
    Args:
        step_name: 步骤名称，如果不提供则使用函数名
        attach_to_allure: 是否附加到Allure报告
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取步骤名称
            current_step_name = step_name or func.__name__
            
            # 查找page参数
            page = None
            for arg in args:
                if hasattr(arg, 'screenshot') and hasattr(arg, 'click'):
                    page = arg
                    break
            
            if not page:
                for value in kwargs.values():
                    if hasattr(value, 'screenshot') and hasattr(value, 'click'):
                        page = value
                        break
            
            if not page:
                log.warning(f"未找到Page对象，跳过截图: {current_step_name}")
                return func(*args, **kwargs)
            
            try:
                # 执行原函数
                result = func(*args, **kwargs)
                
                # 执行后截图（成功）
                screenshot = Screenshot()
                screenshot_path = screenshot.take_step_screenshot(
                    page, 
                    f"{current_step_name}_成功", 
                    f"{func.__module__}.{func.__qualname__}"
                )
                
                # 附加到Allure报告
                if attach_to_allure and screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name=f"步骤截图(成功): {current_step_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    log.info(f"步骤执行成功，截图已保存: {current_step_name}")
                
                return result
                
            except Exception as e:
                # 执行失败时截图
                if page:
                    screenshot = Screenshot()
                    error_screenshot_path = screenshot.take_step_screenshot(
                        page, 
                        f"{current_step_name}_失败", 
                        f"{func.__module__}.{func.__qualname__}"
                    )
                    
                    if attach_to_allure and error_screenshot_path:
                        allure.attach.file(
                            error_screenshot_path,
                            name=f"步骤截图(失败): {current_step_name}",
                            attachment_type=allure.attachment_type.PNG
                        )
                        log.error(f"步骤执行失败，截图已保存: {current_step_name}")
                
                raise e
        
        return wrapper
    return decorator


def allure_step(step_name: str = None, severity: str = None):
    """
    Allure步骤装饰器 - 自动添加Allure步骤和截图
    
    Args:
        step_name: 步骤名称
        severity: 严重程度 (BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_step_name = step_name or func.__name__
            
            # 设置严重程度
            if severity:
                allure.dynamic.severity(getattr(allure.severity_level, severity.upper()))
            
            with allure.step(current_step_name):
                # 使用截图装饰器
                return step_screenshot(current_step_name)(func)(*args, **kwargs)
        
        return wrapper
    return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    失败重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔(秒)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        log.error(f"函数 {func.__name__} 执行失败，已重试 {max_retries} 次")
                        raise e
                    
                    log.warning(f"函数 {func.__name__} 执行失败，第 {attempt + 1} 次重试: {e}")
                    time.sleep(delay)
        
        return wrapper
    return decorator


def video_recording(attach_to_allure: bool = True, save_video: bool = False):
    """
    视频录制装饰器 - 自动为测试步骤添加视频录制
    
    Args:
        attach_to_allure: 是否附加到Allure报告
        save_video: 是否保存视频文件
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 查找page参数
            page = None
            for arg in args:
                if hasattr(arg, 'screenshot') and hasattr(arg, 'click'):
                    page = arg
                    break
            
            if not page:
                for value in kwargs.values():
                    if hasattr(value, 'screenshot') and hasattr(value, 'click'):
                        page = value
                        break
            
            if not page:
                log.warning(f"未找到Page对象，跳过视频录制: {func.__name__}")
                return func(*args, **kwargs)
            
            try:
                # 执行原函数
                result = func(*args, **kwargs)
                
                # 处理视频
                video_manager = VideoManager()
                
                if attach_to_allure:
                    video_manager.attach_video_to_allure(page, func.__name__)
                
                if save_video:
                    video_manager.save_video_with_test_name(page, func.__name__)
                
                return result
                
            except Exception as e:
                # 如果执行失败，也处理视频
                if page:
                    video_manager = VideoManager()
                    if attach_to_allure:
                        video_manager.attach_video_to_allure(page, f"{func.__name__}_失败")
                    if save_video:
                        video_manager.save_video_with_test_name(page, f"{func.__name__}_失败")
                
                raise e
        
        return wrapper
    return decorator


def allure_step_with_video(step_name: str = None, severity: str = None, 
                          attach_video: bool = True, save_video: bool = False):
    """
    Allure步骤装饰器（带视频） - 自动添加Allure步骤、截图和视频
    
    Args:
        step_name: 步骤名称
        severity: 严重程度
        attach_video: 是否附加视频到Allure报告
        save_video: 是否保存视频文件
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_step_name = step_name or func.__name__
            
            # 设置严重程度
            if severity:
                allure.dynamic.severity(getattr(allure.severity_level, severity.upper()))
            
            with allure.step(current_step_name):
                # 使用截图装饰器
                screenshot_result = step_screenshot(current_step_name)(func)(*args, **kwargs)
                
                # 使用视频录制装饰器
                if attach_video or save_video:
                    video_recording(attach_video, save_video)(func)(*args, **kwargs)
                
                return screenshot_result
        
        return wrapper
    return decorator 