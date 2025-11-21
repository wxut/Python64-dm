"""驱动加载详细诊断工具"""
import ctypes
import os
import sys

# 设置UTF-8编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_driver_signature():
    """检查驱动签名"""
    driver_path = "bin/hwid_spoofer_kernel.sys"
    if not os.path.exists(driver_path):
        return False, "驱动文件不存在"
    
    try:
        import subprocess
        result = subprocess.run(
            ['signtool', 'verify', '/pa', driver_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, "驱动已签名"
        else:
            return False, f"驱动未签名或签名无效: {result.stderr}"
    except:
        return None, "无法检查签名(signtool不可用)"

def check_service_status():
    """检查服务状态"""
    try:
        import subprocess
        result = subprocess.run(
            ['sc', 'query', 'HwidSpoofer'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return "无法查询服务状态"

def get_last_error():
    """获取Windows最后错误码"""
    return ctypes.GetLastError()

def main():
    print("=" * 60)
    print("驱动加载详细诊断工具")
    print("=" * 60)
    print()
    
    # 1. 管理员权限
    print("[1/6] 管理员权限检查")
    if is_admin():
        print("  [OK] 已有管理员权限")
    else:
        print("  [X] 缺少管理员权限")
        print("  请以管理员身份运行此脚本")
        return
    print()
    
    # 2. 文件存在性
    print("[2/6] 文件检查")
    # 根据Python架构选择正确的DLL
    is_64bit = sys.maxsize > 2**32
    dll_path = "bin/x64/hwid_api.dll" if is_64bit else "bin/x86/hwid_api.dll"
    driver_path = "bin/hwid_spoofer_kernel.sys"
    
    print(f"  Python架构: {'64位' if is_64bit else '32位'}")
    print(f"  使用DLL: {dll_path}")
    
    if os.path.exists(dll_path):
        print(f"  [OK] DLL存在: {dll_path}")
    else:
        print(f"  [X] DLL不存在: {dll_path}")
        return
    
    if os.path.exists(driver_path):
        size = os.path.getsize(driver_path)
        print(f"  [OK] 驱动存在: {driver_path} ({size} 字节)")
    else:
        print(f"  [X] 驱动不存在: {driver_path}")
        return
    print()
    
    # 3. 驱动签名
    print("[3/6] 驱动签名检查")
    signed, msg = check_driver_signature()
    if signed is True:
        print(f"  [OK] {msg}")
    elif signed is False:
        print(f"  [X] {msg}")
    else:
        print(f"  [?] {msg}")
    print()
    
    # 4. 服务状态
    print("[4/6] 服务状态检查")
    status = check_service_status()
    print(f"  {status}")
    print()
    
    # 5. 尝试加载驱动
    print("[5/6] 尝试加载驱动")
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from python_binding.hwid_wrapper import HWIDSpoofer
        
        spoofer = HWIDSpoofer(dll_path)
        print("  [OK] DLL加载成功")
        
        abs_driver_path = os.path.abspath(driver_path)
        print(f"  尝试初始化驱动: {abs_driver_path}")
        
        # 获取初始化前的错误码
        ctypes.windll.kernel32.SetLastError(0)
        
        result = spoofer.init(abs_driver_path)
        
        # 获取错误码
        error_code = ctypes.windll.kernel32.GetLastError()
        
        if result:
            print("  [OK] 驱动初始化成功!")
            spoofer.cleanup()
        else:
            print(f"  [X] 驱动初始化失败")
            print(f"  Windows错误码: {error_code}")
            print()
            print("  常见错误码含义:")
            error_messages = {
                2: "系统找不到指定的文件",
                5: "拒绝访问",
                31: "连接到系统上的设备没有发挥作用 - 驱动可能未正确签名或被系统阻止",
                123: "文件名、目录名或卷标语法不正确",
                577: "Windows无法验证此文件的数字签名",
                1060: "指定的服务未安装",
                1072: "指定的服务已标记为删除",
                1073: "指定的服务已存在",
                1275: "此驱动程序已被阻止加载",
            }
            if error_code in error_messages:
                print(f"  错误 {error_code}: {error_messages[error_code]}")
            
            # 针对错误31的特殊说明
            if error_code == 31:
                print()
                print("  错误31的常见原因:")
                print("  1. 驱动未正确签名或签名证书未被信任")
                print("  2. 测试签名模式未启用")
                print("  3. 驱动被Windows安全策略阻止")
                print()
                print("  解决方案:")
                print("  1. 启用测试签名模式:")
                print("     bcdedit /set testsigning on")
                print("     (需要重启电脑)")
                print("  2. 安装测试证书:")
                print("     双击 TestDriverCert.cer")
                print("     安装到'受信任的根证书颁发机构'")
                print("  3. 重新签名驱动:")
                print("     运行 sign_driver.bat")
            
            # 针对错误123的特殊说明
            elif error_code == 123:
                print()
                print("  错误123的常见原因:")
                print("  1. 驱动文件路径包含特殊字符或格式不正确")
                print("  2. 驱动文件本身损坏或格式错误")
                print("  3. 驱动与系统架构不匹配(需要x64版本)")
                print()
                print("  建议解决方案:")
                print("  1. 重新编译驱动: compile_driver.bat")
                print("  2. 确认驱动文件完整性")
                print("  3. 检查系统事件查看器获取更多信息")
            
            # 检查事件查看器
            print()
            print("  建议检查:")
            print("  1. 打开'事件查看器' (eventvwr.msc)")
            print("  2. 查看 Windows日志 > 系统")
            print("  3. 查找来源为'Service Control Manager'的错误")
            
    except Exception as e:
        print(f"  [X] 发生异常: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # 6. 建议
    print("[6/6] 诊断建议")
    print()
    if signed is False:
        print("  主要问题: 驱动未正确签名")
        print("  解决方法:")
        print("  1. 运行 sign_driver.bat 签名驱动")
        print("  2. 双击 TestDriverCert.cer 安装证书")
        print("  3. 将证书安装到'受信任的根证书颁发机构'")
        print("  4. 重新运行此诊断工具")
    else:
        print("  可能的问题:")
        print("  1. 驱动签名证书未安装到正确的存储位置")
        print("  2. 系统安全策略阻止了驱动加载")
        print("  3. 驱动文件本身有问题")
        print()
        print("  建议操作:")
        print("  1. 确认证书已安装到'受信任的根证书颁发机构'")
        print("  2. 检查事件查看器中的详细错误信息")
        print("  3. 尝试重新编译和签名驱动")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n未预期的错误: {e}")
        import traceback
        traceback.print_exc()