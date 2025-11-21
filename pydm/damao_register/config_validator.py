"""配置验证模块"""
import os
from typing import Dict, Any, List, Tuple


class ConfigValidator:
    """配置验证器"""
    
    REQUIRED_FIELDS = {
        'register_code': str,
        'machine_count': int,
        'interval_minutes': int,
        'driver_path': str,
        'dm_dll_path': str,
        'dmreg_dll_path': str
    }
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证配置有效性"""
        errors = []
        
        # 检查必需字段
        for field, field_type in ConfigValidator.REQUIRED_FIELDS.items():
            if field not in config:
                errors.append(f"缺少必需配置: {field}")
            elif not isinstance(config[field], field_type):
                errors.append(f"配置类型错误: {field} 应为 {field_type.__name__}")
        
        # 检查数值范围
        if 'machine_count' in config:
            if not (1 <= config['machine_count'] <= 100):
                errors.append("机器数量应在1-100之间")
        
        if 'interval_minutes' in config:
            if not (1 <= config['interval_minutes'] <= 1440):
                errors.append("注册间隔应在1-1440分钟之间")
        
        # 检查文件路径
        file_paths = ['driver_path', 'dm_dll_path', 'dmreg_dll_path']
        for path_field in file_paths:
            if path_field in config:
                if not os.path.exists(config[path_field]):
                    errors.append(f"文件不存在: {config[path_field]}")
        
        return len(errors) == 0, errors