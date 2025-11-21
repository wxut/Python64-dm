"""最终参数传递验证"""
import subprocess
import time

def verify_parameter_passing():
    """验证参数传递"""
    try:
        # 清理进程
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(1)
        
        # 直接测试桥接客户端
        from damao_bridge_client_optimized import DaMaoBridgeClientOptimized
        
        reg_code = "270207756caf4b32039fc35397d603f9688eaa665"
        ver_info = "x2ImSD03b7"
        
        client = DaMaoBridgeClientOptimized(reg_code, ver_info)
        
        if client.start_server():
            response = client.create()
            if response.get('success'):
                print(f"✓ 参数传递验证成功")
                print(f"  注册码: {response.get('reg_code', 'N/A')}")
                print(f"  对象ID: {response.get('object_id', 'N/A')}")
                print(f"  注册结果: {response.get('reg_result', 'N/A')}")
                client.shutdown()
                return True
        
        print("✗ 参数传递验证失败")
        return False
        
    except Exception as e:
        print(f"验证异常: {e}")
        return False

if __name__ == "__main__":
    success = verify_parameter_passing()
    exit(0 if success else 1)