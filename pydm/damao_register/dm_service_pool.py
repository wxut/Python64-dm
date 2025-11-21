"""大漠服务进程池管理"""
import queue
import threading
from typing import Optional
from . import logger
from .damao_wrapper import DaMaoWrapper


class DmServicePool:
    """大漠服务进程池"""
    
    def __init__(self, pool_size: int = 2):
        self.pool_size = pool_size
        self.available_services = queue.Queue(maxsize=pool_size)
        self.all_services = []
        self.lock = threading.Lock()
        self.log = logger.get_logger()
        self.service_counter = 0  # 服务计数器，避免重复日志
        self._init_pool()
    
    def _init_pool(self):
        """初始化进程池"""
        for _ in range(self.pool_size):
            service = self._create_service()
            if service:
                self.available_services.put(service)
                self.all_services.append(service)
    
    def _create_service(self) -> Optional[DaMaoWrapper]:
        """创建新的服务实例"""
        try:
            service = DaMaoWrapper()
            # 只为第一个服务实例输出日志
            if service.create():
                if self.service_counter == 0:
                    self.log.info("DmService32服务池初始化完成")
                self.service_counter += 1
                return service
        except Exception as e:
            self.log.error(f"创建服务失败: {e}")
        return None
    
    def get_service(self) -> Optional[DaMaoWrapper]:
        """获取可用服务"""
        try:
            return self.available_services.get(timeout=5)
        except queue.Empty:
            return self._create_service()
    
    def return_service(self, service: DaMaoWrapper):
        """归还服务到池中"""
        try:
            self.available_services.put(service, timeout=1)
        except queue.Full:
            # 池已满，直接释放
            service.release()
    
    def cleanup(self):
        """清理所有服务"""
        with self.lock:
            if self.all_services:
                self.log.info("清理服务池中的所有服务")
            for service in self.all_services:
                try:
                    service.release()
                except:
                    pass
            self.all_services.clear()
            self.service_counter = 0