import subprocess
import sys

driver_path = "bin/hwid_spoofer_kernel.sys"

print("检查驱动签名状态...")
print(f"驱动文件: {driver_path}")
print()

try:
    # 使用 certutil 检查签名
    result = subprocess.run(
        ['certutil', '-verify', driver_path],
        capture_output=True,
        text=True,
        encoding='gbk'
    )
    
    print("=== certutil 输出 ===")
    print(result.stdout)
    if result.stderr:
        print("错误信息:")
        print(result.stderr)
    
    print()
    print(f"返回码: {result.returncode}")
    
    if result.returncode == 0:
        print("\n✅ 驱动签名验证成功")
    else:
        print("\n❌ 驱动签名验证失败")
        
except Exception as e:
    print(f"检查失败: {e}")