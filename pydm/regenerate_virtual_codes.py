"""重新生成虚拟机器码工具"""
import json
import random
import string
from pathlib import Path


def generate_virtual_machine_code() -> str:
    """生成新的虚拟机器码（32位格式）"""
    segments = []
    for _ in range(4):
        segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        segments.append(segment)
    return '-'.join(segments)


def regenerate_codes():
    """重新生成所有配置的虚拟机器码"""
    config_path = Path("config/hwid_profiles.json")
    
    # 读取现有配置
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 为每个配置生成新的虚拟机器码
    for profile in data['profiles']:
        old_code = profile.get('virtual_machine_code', '')
        new_code = generate_virtual_machine_code()
        profile['virtual_machine_code'] = new_code
        profile['register_count'] = 0  # 重置注册次数
        
        print(f"配置 {profile['id']} ({profile['product_name']})")
        print(f"  旧虚拟码: {old_code}")
        print(f"  新虚拟码: {new_code}")
        print()
    
    # 保存更新后的配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 已更新 {len(data['profiles'])} 个配置的虚拟机器码")
    print(f"✓ 配置文件已保存: {config_path}")


if __name__ == "__main__":
    regenerate_codes()