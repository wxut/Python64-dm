"""修复大漠对象创建失败问题"""
import subprocess
import time
import os

def kill_existing_processes():
    """清理可能冲突的进程"""
    try:
        # 杀死所有32位Python进程
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(1)
    except:
        pass

def test_dm_creation():
    """测试大漠对象创建"""
    from damao_wrapper_optimized import DaMaoWrapperOptimized
    
    # 清理进程
    kill_existing_processes()
    
    reg_code = "270207756caf4b32039fc35397d603f9688eaa665"
    ver_info = "x2ImSD03b7"
    
    dm = DaMaoWrapperOptimized(reg_code, ver_info)
    
    print("尝试创建大漠对象...")
    success = dm.create()
    
    if success:
        print("✓ 创建成功")
        machine_code = dm.get_machine_code()
        print(f"机器码: {machine_code}")
        dm.release()
    else:
        print("✗ 创建失败")
    
    return success

if __name__ == "__main__":
    test_dm_creation()