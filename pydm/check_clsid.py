"""检查 CLSID 注册信息"""
import winreg

clsid = "{26037A0E-7CBD-4FFF-9C63-56F2D0770214}"

print("=" * 60)
print(f"Checking CLSID: {clsid}")
print("=" * 60)
print()

try:
    # 检查 CLSID 在注册表中的信息
    key_path = f"CLSID\\{clsid}"
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path)
    print(f"[OK] CLSID found in registry")
    
    # 尝试读取 InprocServer32
    try:
        inproc_key = winreg.OpenKey(key, "InprocServer32")
        dll_path, _ = winreg.QueryValueEx(inproc_key, "")
        print(f"[OK] InprocServer32: {dll_path}")
        
        # 检查 ThreadingModel
        try:
            threading, _ = winreg.QueryValueEx(inproc_key, "ThreadingModel")
            print(f"[OK] ThreadingModel: {threading}")
        except:
            print(f"[X] No ThreadingModel specified")
        
        winreg.CloseKey(inproc_key)
    except Exception as e:
        print(f"[X] Cannot read InprocServer32: {e}")
    
    winreg.CloseKey(key)
except Exception as e:
    print(f"[X] CLSID not found or error: {e}")