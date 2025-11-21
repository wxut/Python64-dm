"""统一异常处理模块"""
import time
import functools
from typing import Callable, Any


class DmException(Exception):
    """大漠系统异常基类"""
    def __init__(self, code: int, message: str, details: str = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"[{code}] {message}")


class ErrorCodes:
    """错误代码定义"""
    DRIVER_INIT_FAILED = 1001
    DM_REGISTER_FAILED = 1002
    HWID_APPLY_FAILED = 1003
    SERVICE_UNAVAILABLE = 1004
    CONFIG_INVALID = 1005


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator