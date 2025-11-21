import ctypes
import os

class HWIDSpoofer:
    def __init__(self, dll_path="hwid_api.dll"):
        self.dll = ctypes.CDLL(dll_path)
        
        # 定义函数签名
        self.dll.hwid_init.argtypes = [ctypes.c_wchar_p]
        self.dll.hwid_init.restype = ctypes.c_int
        
        self.dll.hwid_cleanup.argtypes = []
        self.dll.hwid_cleanup.restype = None
        
        self.dll.hwid_set_smbios.argtypes = [ctypes.c_char_p] * 8
        self.dll.hwid_set_smbios.restype = ctypes.c_int
        
        self.dll.hwid_set_disk.argtypes = [ctypes.c_char_p] * 3
        self.dll.hwid_set_disk.restype = ctypes.c_int
        
        self.dll.hwid_set_disk_guid_random.argtypes = [ctypes.c_int]
        self.dll.hwid_set_disk_guid_random.restype = ctypes.c_int
        
        self.dll.hwid_set_disk_volume_clean.argtypes = [ctypes.c_int]
        self.dll.hwid_set_disk_volume_clean.restype = ctypes.c_int
        
        self.dll.hwid_set_mac_random.argtypes = []
        self.dll.hwid_set_mac_random.restype = ctypes.c_int
        
        self.dll.hwid_set_mac_custom.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.dll.hwid_set_mac_custom.restype = ctypes.c_int
        
        self.dll.hwid_set_gpu_serial.argtypes = [ctypes.c_char_p]
        self.dll.hwid_set_gpu_serial.restype = ctypes.c_int
        
        self.dll.hwid_set_arp_table_handle.argtypes = [ctypes.c_int]
        self.dll.hwid_set_arp_table_handle.restype = ctypes.c_int
        
        self.dll.hwid_set_cpuid.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.dll.hwid_set_cpuid.restype = ctypes.c_int
        
        self.dll.hwid_enable_vm_spoof.argtypes = [ctypes.c_int]
        self.dll.hwid_enable_vm_spoof.restype = ctypes.c_int
        
        self.dll.hwid_set_cpu_vendor.argtypes = [ctypes.c_char_p]
        self.dll.hwid_set_cpu_vendor.restype = ctypes.c_int
    
    def init(self, driver_path):
        return self.dll.hwid_init(driver_path) == 1
    
    def cleanup(self):
        self.dll.hwid_cleanup()
    
    def set_smbios(self, vendor, version, date, manufacturer, product_name, serial_number, uuid=None, board_serial=None):
        # 处理uuid - 如果是hex字符串则转换为bytes，如果是None则用空字节
        if uuid is None:
            uuid_bytes = b'\x00' * 16
        elif isinstance(uuid, str) and len(uuid) == 32:  # hex字符串
            uuid_bytes = bytes.fromhex(uuid)
        elif isinstance(uuid, bytes):
            uuid_bytes = uuid
        else:
            uuid_bytes = uuid.encode() if isinstance(uuid, str) else b'\x00' * 16
        
        # 处理board_serial - 如果是字符串则编码，如果是None则用空字节
        if board_serial is None:
            board_serial_bytes = b''
        else:
            board_serial_bytes = board_serial.encode() if isinstance(board_serial, str) else board_serial
        
        return self.dll.hwid_set_smbios(
            vendor.encode(), version.encode(), date.encode(),
            manufacturer.encode(), product_name.encode(), serial_number.encode(),
            uuid_bytes, board_serial_bytes
        ) == 1
    
    def set_disk(self, serial, model, revision):
        return self.dll.hwid_set_disk(
            serial.encode(), model.encode(), revision.encode()
        ) == 1
    
    def set_disk_guid_random(self, enable):
        return self.dll.hwid_set_disk_guid_random(1 if enable else 0) == 1
    
    def set_disk_volume_clean(self, enable):
        return self.dll.hwid_set_disk_volume_clean(1 if enable else 0) == 1
    
    def set_mac_random(self):
        return self.dll.hwid_set_mac_random() == 1
    
    def set_mac_custom(self, permanent, current):
        return self.dll.hwid_set_mac_custom(
            permanent.encode(), current.encode()
        ) == 1
    
    def set_gpu_serial(self, serial):
        return self.dll.hwid_set_gpu_serial(serial.encode()) == 1
    
    def set_arp_table_handle(self, enable):
        return self.dll.hwid_set_arp_table_handle(1 if enable else 0) == 1
    
    def set_cpuid(self, cpuid_0, cpuid_1):
        return self.dll.hwid_set_cpuid(cpuid_0.encode(), cpuid_1.encode()) == 1
    
    def enable_vm_spoof(self, enable):
        """启用/禁用虚拟机伪装"""
        return self.dll.hwid_enable_vm_spoof(1 if enable else 0) == 1
    
    def set_cpu_vendor(self, vendor):
        """设置CPU厂商字符串"""
        return self.dll.hwid_set_cpu_vendor(vendor.encode()) == 1

# 使用示例
if __name__ == "__main__":
    spoofer = HWIDSpoofer("hwid_api.dll")
    
    if spoofer.init(r"C:\path\to\driver.sys"):
        print("驱动初始化成功")
        
        # 设置SMBIOS信息
        spoofer.set_smbios("ASUS", "1.0", "01/01/2023", "ASUS", "ROG", "ABC123")
        
        # 设置磁盘信息
        spoofer.set_disk("DISK123", "Samsung SSD", "1.0")
        
        # 设置MAC地址随机
        spoofer.set_mac_random()
        
        spoofer.cleanup()
        print("清理完成")
    else:
        print("驱动初始化失败")