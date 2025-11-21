"""清理启动脚本 - 确保无冲突启动"""
import subprocess
import time
import sys

def clean_start():
    """清理并启动程序"""
    print("清理可能的冲突进程...")
    
    # 终止所有Python进程
    try:
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        print("✅ 进程清理完成")
    except:
        print("⚠️ 清理过程中出现异常，继续启动")
    
    # 启动主程序
    print("启动主程序...")
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        subprocess.run([sys.executable, script_name])
    else:
        subprocess.run([sys.executable, 'main.py'])

if __name__ == "__main__":
    clean_start()