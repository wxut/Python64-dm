"""统一日志管理模块"""
import logging
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler


class Logger:
    """日志管理器"""
    
    def __init__(self, name: str = "DaMaoRegister", 
                 log_dir: str = "logs",
                 log_file: str = "register.log",
                 level: str = "INFO",
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        """
        初始化日志管理器
        
        Args:
            name: 日志记录器名称
            log_dir: 日志目录
            log_file: 日志文件名
            level: 日志级别
            max_bytes: 单个日志文件最大大小
            backup_count: 保留的日志文件数量
        """
        self.name = name
        self.log_dir = log_dir
        self.log_file = log_file
        self.level = getattr(logging, level.upper(), logging.INFO)
        
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # 避免重复添加处理器
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 禁用文件日志输出
        # log_path = os.path.join(log_dir, log_file)
        # file_handler = RotatingFileHandler(
        #     log_path,
        #     maxBytes=max_bytes,
        #     backupCount=backup_count,
        #     encoding='utf-8'
        # )
        # file_handler.setLevel(self.level)
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, msg: str):
        """调试日志"""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """信息日志"""
        self.logger.info(msg)
    
    def warning(self, msg: str):
        """警告日志"""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """错误日志"""
        self.logger.error(msg)
    
    def critical(self, msg: str):
        """严重错误日志"""
        self.logger.critical(msg)
    
    def exception(self, msg: str):
        """异常日志（包含堆栈信息）"""
        self.logger.exception(msg)
    
    def set_level(self, level: str):
        """设置日志级别"""
        new_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(new_level)
        for handler in self.logger.handlers:
            handler.setLevel(new_level)
        self.level = new_level
    
    def log_separator(self, char: str = "=", length: int = 60):
        """记录分隔线"""
        self.info(char * length)
    
    def log_section(self, title: str):
        """记录章节标题"""
        self.log_separator()
        self.info(f"  {title}")
        self.log_separator()
    
    def log_hwid_info(self, profile: dict):
        """记录硬件信息"""
        self.info("应用硬件配置:")
        self.info(f"  SMBIOS: {profile.get('manufacturer', 'N/A')} {profile.get('product_name', 'N/A')}")
        self.info(f"  序列号: {profile.get('serial_number', 'N/A')}")
        self.info(f"  磁盘: {profile.get('disk_model', 'N/A')}")
        self.info(f"  磁盘序列号: {profile.get('disk_serial', 'N/A')}")
    
    def log_register_result(self, success: bool, version: str = "", 
                           machine_code: str = "", mouse_pos: tuple = (0, 0)):
        """记录注册结果"""
        if success:
            self.info("注册成功")
            self.info(f"  版本: {version}")
            self.info(f"  机器码: {machine_code}")
            self.info(f"  鼠标位置: {mouse_pos}")
        else:
            self.error("注册失败")
    
    def log_driver_status(self, installed: bool, error: str = ""):
        """记录驱动状态"""
        if installed:
            self.info("驱动加载成功")
        else:
            self.error(f"驱动加载失败: {error}")
    
    def log_cycle_info(self, current: int, total: int, next_time: Optional[datetime] = None):
        """记录循环信息"""
        self.info(f"当前进度: {current}/{total}")
        if next_time:
            self.info(f"下次注册时间: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def log_simple_registration(self, machine_code: str, log_file: str = "logs/simple_register.log"):
        """简洁注册日志 - 整合simple_logger功能"""
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 读取现有内容并更新计数
        lines = []
        machine_counts = {}
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # 统计现有计数
        for line in lines:
            if line.strip() and ',' in line:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    code = parts[1]
                    count = int(parts[2])
                    machine_counts[code] = count
        
        # 更新当前机器码计数
        machine_counts[machine_code] = machine_counts.get(machine_code, 0) + 1
        count = machine_counts[machine_code]
        
        # 更新文件
        found = False
        for i, line in enumerate(lines):
            if line.strip() and machine_code in line:
                lines[i] = f"{timestamp},{machine_code},{count}\n"
                found = True
                break
        
        if not found:
            lines.append(f"{timestamp},{machine_code},{count}\n")
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)


# 全局日志实例
_global_logger: Optional[Logger] = None


def get_logger(name: str = "DaMaoRegister", 
               log_dir: str = "logs",
               log_file: str = "register.log",
               level: str = "INFO") -> Logger:
    """获取全局日志实例"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger(name, log_dir, log_file, level)
    return _global_logger


def set_log_level(level: str):
    """设置全局日志级别"""
    logger = get_logger()
    logger.set_level(level)


# 便捷函数
def debug(msg: str):
    """调试日志"""
    get_logger().debug(msg)


def info(msg: str):
    """信息日志"""
    get_logger().info(msg)


def warning(msg: str):
    """警告日志"""
    get_logger().warning(msg)


def error(msg: str):
    """错误日志"""
    get_logger().error(msg)


def critical(msg: str):
    """严重错误日志"""
    get_logger().critical(msg)


def exception(msg: str):
    """异常日志"""
    get_logger().exception(msg)