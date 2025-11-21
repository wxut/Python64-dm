"""硬件信息生成器"""
import random
import string
from typing import Dict, List, Any


class HWIDGenerator:
    """硬件信息生成器"""
    
    # 常见的主板厂商
    VENDORS = ["ASUS", "MSI", "GIGABYTE", "ASRock", "EVGA"]
    
    # 常见的主板型号
    BOARD_MODELS = [
        "ROG STRIX", "TUF GAMING", "PRIME", "PRO",
        "GAMING EDGE", "TOMAHAWK", "MORTAR",
        "AORUS", "GAMING", "UD",
        "Phantom Gaming", "Steel Legend"
    ]
    
    # 常见的磁盘型号
    DISK_MODELS = [
        "Samsung SSD 970", "Samsung SSD 980", "WD Blue",
        "Crucial MX500", "Kingston A2000", "Seagate Barracuda"
    ]
    
    # CPU厂商标识
    CPU_VENDORS = ["GenuineIntel", "AuthenticAMD"]
    
    @staticmethod
    def generate_serial(length: int = 12) -> str:
        """生成随机序列号"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    @staticmethod
    def generate_virtual_machine_code() -> str:
        """生成虚拟机器码（32位格式）
        
        大漠插件的机器码格式通常为：XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX
        每段8个字符，共4段，用连字符分隔
        """
        segments = []
        for _ in range(4):
            segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            segments.append(segment)
        return '-'.join(segments)
    
    @staticmethod
    def generate_profile() -> Dict[str, Any]:
        """生成单个硬件配置"""
        vendor = random.choice(HWIDGenerator.VENDORS)
        board_model = random.choice(HWIDGenerator.BOARD_MODELS)
        disk_model = random.choice(HWIDGenerator.DISK_MODELS)
        cpu_vendor = random.choice(HWIDGenerator.CPU_VENDORS)
        
        # 生成UUID (16字节) - 转换为hex字符串以支持JSON序列化
        uuid_bytes = bytes([random.randint(0, 255) for _ in range(16)])
        system_uuid = uuid_bytes.hex()
        
        return {
            "vendor": vendor,
            "version": f"{random.randint(1, 9)}.{random.randint(0, 99)}",
            "date": f"{random.randint(1, 12):02d}/{random.randint(1, 28):02d}/20{random.randint(20, 24)}",
            "manufacturer": vendor,
            "product_name": f"{vendor} {board_model}",
            "serial_number": HWIDGenerator.generate_serial(12),
            "system_uuid": system_uuid,
            "board_serial": HWIDGenerator.generate_serial(12),
            "disk_serial": HWIDGenerator.generate_serial(20),
            "disk_model": disk_model,
            "disk_revision": f"{random.randint(1, 9)}.{random.randint(0, 9)}",
            "cpuid_0": cpu_vendor,
            "cpuid_1": f"0x{random.randint(0x00800000, 0x00FFFFFF):08X}",
            "virtual_machine_code": HWIDGenerator.generate_virtual_machine_code()
        }
    
    @staticmethod
    def generate_profiles(count: int) -> List[Dict[str, Any]]:
        """生成多个硬件配置"""
        profiles = []
        for i in range(count):
            profile = HWIDGenerator.generate_profile()
            profile["id"] = i + 1
            profiles.append(profile)
        return profiles