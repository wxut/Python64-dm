"""配置管理模块"""
import json
import os
import sys
import platform
from typing import Dict, List, Any, Optional
from .config_validator import ConfigValidator


class ConfigManager:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "machine_count": 5,
        "interval_minutes": 120,
        "max_register_count": 2,
        "driver_path": "bin/x64/hwid_spoofer_kernel.sys",
        "dll_path_x64": "bin/x64/hwid_api.dll",
        "dll_path_x86": "bin/x86/hwid_api.dll",
        "dm_dll_path": "bin/dm.dll",
        "dmreg_dll_path": "bin/dmreg.dll",
        "register_code": "",
        "additional_code": "",
        "auto_start": False,
        "log_level": "INFO"
    }
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._ensure_config_exists()
        self.load()
    
    def _ensure_config_exists(self):
        """确保配置文件存在"""
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    
    def load(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            # 合并默认配置，确保所有必需的键都存在
            for key, value in self.DEFAULT_CONFIG.items():
                if key not in self.config:
                    self.config[key] = value
            
            # 验证配置
            is_valid, errors = ConfigValidator.validate_config(self.config)
            if not is_valid:
                print(f"配置验证失败: {'; '.join(errors)}")
            
            return self.config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.config = self.DEFAULT_CONFIG.copy()
            return self.config
    
    def save(self) -> bool:
        """保存配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        self.config[key] = value
    
    def get_dmreg_dll_path(self) -> str:
        """获取dmreg.dll路径"""
        return self.config.get("dmreg_dll_path", "bin/dmreg.dll")
    
    def get_register_code(self) -> str:
        """获取注册码"""
        return self.config.get("register_code", "")
    
    def set_register_code(self, code: str) -> bool:
        """设置注册码"""
        self.config["register_code"] = code
        return self.save()
    
    def get_additional_code(self) -> str:
        """获取附加码"""
        return self.config.get("additional_code", "")
    
    def set_additional_code(self, code: str) -> bool:
        """设置附加码"""
        self.config["additional_code"] = code
        return self.save()
    
    def get_machine_count(self) -> int:
        """获取机器数量"""
        return self.config.get("machine_count", 5)
    
    def set_machine_count(self, count: int) -> bool:
        """设置机器数量"""
        if 1 <= count <= 100:
            self.config["machine_count"] = count
            return self.save()
        return False
    
    def get_interval_hours(self) -> float:
        """获取注册间隔（小时）- 已弃用，保留用于兼容"""
        return self.config.get("interval_hours", 2)
    
    def set_interval_hours(self, hours: float) -> bool:
        """设置注册间隔（小时）- 已弃用，保留用于兼容"""
        if hours > 0:
            self.config["interval_hours"] = hours
            return self.save()
        return False
    
    def get_interval_minutes(self) -> int:
        """获取注册间隔（分钟）"""
        # 兼容旧配置
        if "interval_hours" in self.config and "interval_minutes" not in self.config:
            return int(self.config.get("interval_hours", 2) * 60)
        return self.config.get("interval_minutes", 120)
    
    def set_interval_minutes(self, minutes: int) -> bool:
        """设置注册间隔（分钟）"""
        if 1 <= minutes <= 120:
            self.config["interval_minutes"] = minutes
            return self.save()
        return False
    
    
    def get_driver_path(self) -> str:
        """获取驱动路径"""
        return self.config.get("driver_path", "bin/hwid_spoofer_kernel.sys")
    
    def get_dll_path(self) -> str:
        """获取DLL路径（自动根据Python架构选择）"""
        # 检测Python架构
        is_64bit = sys.maxsize > 2**32
        
        if is_64bit:
            # 64位Python使用64位DLL
            return self.config.get("dll_path_x64", "bin/x64/hwid_api.dll")
        else:
            # 32位Python使用32位DLL
            return self.config.get("dll_path_x86", "bin/x86/hwid_api.dll")
    
    def get_dm_dll_path(self) -> str:
        """获取大漠DLL路径"""
        return self.config.get("dm_dll_path", "bin/dm.dll")
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.config.get("log_level", "INFO")
    
    def set_log_level(self, level: str) -> bool:
        """设置日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level.upper() in valid_levels:
            self.config["log_level"] = level.upper()
            return self.save()
        return False
    
    def is_auto_start(self) -> bool:
        """是否自动启动"""
        return self.config.get("auto_start", False)
    
    def set_auto_start(self, auto_start: bool) -> bool:
        """设置自动启动"""
        self.config["auto_start"] = auto_start
        return self.save()
    
    def get_max_register_count(self) -> int:
        """获取单个机器码最大注册次数"""
        return self.config.get("max_register_count", 2)
    
    def set_max_register_count(self, count: int) -> bool:
        """设置单个机器码最大注册次数"""
        if count > 0:
            self.config["max_register_count"] = count
            return self.save()
        return False


class HWIDProfileManager:
    """硬件信息配置管理器"""
    
    def __init__(self, profile_path: str = "config/hwid_profiles.json"):
        self.profile_path = profile_path
        self.profiles: List[Dict[str, Any]] = []
        self._ensure_profile_exists()
        self.load()
    
    def _ensure_profile_exists(self):
        """确保配置文件存在"""
        if not os.path.exists(self.profile_path):
            os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump({"profiles": []}, f, indent=2, ensure_ascii=False)
    
    def load(self) -> List[Dict[str, Any]]:
        """加载硬件配置"""
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.profiles = data.get("profiles", [])
            return self.profiles
        except Exception as e:
            print(f"加载硬件配置文件失败: {e}")
            self.profiles = []
            return self.profiles
    
    def save(self) -> bool:
        """保存硬件配置"""
        try:
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump({"profiles": self.profiles}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存硬件配置文件失败: {e}")
            return False
    
    def add_profile(self, profile: Dict[str, Any]) -> bool:
        """添加硬件配置"""
        if not profile.get("id"):
            # 自动生成ID
            profile["id"] = len(self.profiles) + 1
        self.profiles.append(profile)
        return self.save()
    
    def remove_profile(self, profile_id: int) -> bool:
        """删除硬件配置"""
        self.profiles = [p for p in self.profiles if p.get("id") != profile_id]
        return self.save()
    
    def get_profile(self, profile_id: int) -> Optional[Dict[str, Any]]:
        """获取指定硬件配置"""
        for profile in self.profiles:
            if profile.get("id") == profile_id:
                return profile
        return None
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """获取所有硬件配置"""
        return self.profiles
    
    def clear_profiles(self) -> bool:
        """清空所有硬件配置"""
        self.profiles = []
        return self.save()
    
    def update_profile(self, profile_id: int, profile: Dict[str, Any]) -> bool:
        """更新硬件配置"""
        for i, p in enumerate(self.profiles):
            if p.get("id") == profile_id:
                profile["id"] = profile_id
                self.profiles[i] = profile
                return self.save()
        return False