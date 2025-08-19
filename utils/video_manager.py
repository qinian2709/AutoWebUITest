"""
视频管理工具类
"""
import os
import shutil
from datetime import datetime
from typing import Optional
from playwright.sync_api import Page
from utils.logger import log
import allure


class VideoManager:
    """视频管理工具类"""
    
    def __init__(self, reports_dir: str = "./reports"):
        self.reports_dir = reports_dir
        self.videos_dir = os.path.join(reports_dir, "videos")
        self._ensure_video_dir()
    
    def _ensure_video_dir(self):
        """确保视频目录存在"""
        os.makedirs(self.videos_dir, exist_ok=True)
    
    def get_video_path(self, page: Page) -> Optional[str]:
        """获取视频文件路径"""
        try:
            if page.video:
                return page.video.path()
            return None
        except Exception as e:
            log.warning(f"获取视频路径失败: {e}")
            return None
    
    def attach_video_to_allure(self, page: Page, test_name: str = None):
        """将视频附加到Allure报告"""
        try:
            video_path = self.get_video_path(page)
            if video_path and os.path.exists(video_path):
                # 附加视频到Allure报告
                allure.attach.file(
                    video_path,
                    name=f"测试执行视频 - {test_name or '未知测试'}",
                    attachment_type=allure.attachment_type.MP4
                )
                log.info(f"视频已附加到Allure报告: {video_path}")
                return True
            else:
                log.warning("未找到视频文件或视频文件不存在")
                return False
        except Exception as e:
            log.error(f"附加视频到Allure报告失败: {e}")
            return False
    
    def save_video_with_test_name(self, page: Page, test_name: str) -> Optional[str]:
        """保存视频文件并重命名"""
        try:
            video_path = self.get_video_path(page)
            if video_path and os.path.exists(video_path):
                # 生成新的文件名 - 使用MP4格式
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{test_name}_{timestamp}.mp4"
                new_path = os.path.join(self.videos_dir, new_filename)
                
                # 复制视频文件
                shutil.copy2(video_path, new_path)
                log.info(f"视频已保存为MP4格式: {new_path}")
                return new_path
            return None
        except Exception as e:
            log.error(f"保存视频文件失败: {e}")
            return None
    
    def cleanup_old_videos(self, max_age_hours: int = 24):
        """清理旧的视频文件"""
        try:
            current_time = datetime.now()
            count = 0
            
            for filename in os.listdir(self.videos_dir):
                file_path = os.path.join(self.videos_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > max_age_hours:
                        os.remove(file_path)
                        count += 1
                        log.info(f"删除旧视频文件: {filename}")
            
            if count > 0:
                log.info(f"清理了 {count} 个旧视频文件")
        except Exception as e:
            log.error(f"清理旧视频文件失败: {e}")
    
    def get_video_info(self, video_path: str) -> dict:
        """获取视频文件信息"""
        try:
            if os.path.exists(video_path):
                stat = os.stat(video_path)
                return {
                    "path": video_path,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime),
                    "modified": datetime.fromtimestamp(stat.st_mtime)
                }
            return {}
        except Exception as e:
            log.error(f"获取视频信息失败: {e}")
            return {} 