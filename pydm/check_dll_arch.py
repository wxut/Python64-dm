import struct

def check_dll_architecture(dll_path):
    """检查DLL是32位还是64位"""
    try:
        with open(dll_path, 'rb') as f:
            # 读取DOS头
            dos_header = f.read(64)
            # 获取PE头偏移
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            
            # 跳到PE头
            f.seek(pe_offset)
            # 读取PE签名和COFF头
            pe_sig = f.read(4)
            coff_header = f.read(20)
            
            # 获取机器类型
            machine = struct.unpack('<H', coff_header[0:2])[0]
            
            if machine == 0x014c:
                return "32位 (x86)"
            elif machine == 0x8664:
                return "64位 (x64)"
            else:
                return f"未知架构 (0x{machine:04x})"
    except Exception as e:
        return f"检查失败: {e}"

# 检查所有DLL
dlls = [
    "bin/hwid_api.dll",
    "bin/dm.dll",
    "bin/DmReg.dll"
]

print("DLL架构检查:")
print("=" * 50)
for dll in dlls:
    arch = check_dll_architecture(dll)
    print(f"{dll}: {arch}")

# 检查当前Python架构
import sys
python_arch = "64位" if sys.maxsize > 2**32 else "32位"
print("=" * 50)
print(f"当前Python: {python_arch}")