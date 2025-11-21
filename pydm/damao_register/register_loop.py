"""注册循环逻辑模块"""
import sys
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from python_binding.hwid_wrapper import HWIDSpoofer
# 使用优化的大漠包装器
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from .damao_wrapper import DaMaoWrapper
from .dm_service_pool import DmServicePool
from .config_manager import ConfigManager, HWIDProfileManager
from .hwid_generator import HWIDGenerator
from . import logger
import random
import time


class RegisterLoop:
    """注册循环控制器"""
    
    def __init__(self, config_manager: ConfigManager, profile_manager: HWIDProfileManager):
        self.config = config_manager
        self.profile_mgr = profile_manager
        self.log = logger.get_logger()
        self.running = False
        self.spoofer: Optional[HWIDSpoofer] = None
        self.profiles: List[Dict[str, Any]] = []
        self.dm_pool = None  # 大漠服务池
        self.current_profile_id = None  # 当前应用的硬件配置ID
        self.machine_register_counts = {}  # 机器码注册次数统计
        
    def initialize(self) -> bool:
        """初始化系统"""
        self.log.log_section("系统初始化")
        
        # 初始化hwid_api.dll
        dll_path = self.config.get_dll_path()
        driver_path = self.config.get_driver_path()
        
        # 转换为绝对路径并规范化为Windows格式（使用反斜杠）
        abs_driver_path = os.path.abspath(driver_path).replace('/', '\\')
        
        self.log.info(f"加载DLL: {dll_path}")
        self.log.info(f"驱动路径: {driver_path}")
        self.log.info(f"驱动绝对路径: {abs_driver_path}")
        
        try:
            self.spoofer = HWIDSpoofer(dll_path)
            if not self.spoofer.init(abs_driver_path):
                self.log.error("驱动初始化失败")
                return False
            self.log.log_driver_status(True)
        except Exception as e:
            self.log.error(f"初始化异常: {e}")
            return False
        
        # 生成或加载硬件配置
        self.profiles = self.profile_mgr.get_all_profiles()
        if not self.profiles:
            machine_count = self.config.get_machine_count()
            self.log.info(f"生成{machine_count}个硬件配置")
            self.profiles = HWIDGenerator.generate_profiles(machine_count)
            for profile in self.profiles:
                self.profile_mgr.add_profile(profile)
        
        self.log.info(f"加载了{len(self.profiles)}个硬件配置")
        return True
    
    def apply_hwid_profile(self, profile: Dict[str, Any]) -> bool:
        """应用硬件配置"""
        try:
            # 移除详细硬件信息日志输出
            
            # 设置SMBIOS (包含UUID和主板序列号)
            self.spoofer.set_smbios(
                vendor=profile.get('vendor', ''),
                version=profile.get('version', ''),
                date=profile.get('date', ''),
                manufacturer=profile.get('manufacturer', ''),
                product_name=profile.get('product_name', ''),
                serial_number=profile.get('serial_number', ''),
                uuid=profile.get('system_uuid'),
                board_serial=profile.get('board_serial')
            )
            
            # 设置磁盘信息
            self.spoofer.set_disk(
                serial=profile.get('disk_serial', ''),
                model=profile.get('disk_model', ''),
                revision=profile.get('disk_revision', '')
            )
            
            # 设置磁盘卷序列号清除
            self.spoofer.set_disk_volume_clean(1)
            
            # 设置CPUID
            self.spoofer.set_cpuid(
                cpuid_0=profile.get('cpuid_0', 'GenuineIntel'),
                cpuid_1=profile.get('cpuid_1', '0x000906E9')
            )
            
            # 设置随机MAC
            self.spoofer.set_mac_random()
            
            # 启用虚拟机伪装
            self.spoofer.enable_vm_spoof(1)
            
            return True
        except Exception as e:
            self.log.error(f"应用硬件配置失败: {e}")
            return False
    
    def init_dm_pool(self) -> bool:
        """初始化大漠服务池"""
        if not self.dm_pool:
            self.dm_pool = DmServicePool(pool_size=2)
        return True
    
    def cleanup_dm_pool(self):
        """清理大漠服务池"""
        if self.dm_pool:
            self.dm_pool.cleanup()
            self.dm_pool = None
    
    def register_once(self, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """单次注册流程（每次切换硬件配置时重新创建大漠对象）"""
        profile_id = profile.get('id')
        
        # 只在切换到新机器时应用硬件配置
        if self.current_profile_id != profile_id:
            if not self.apply_hwid_profile(profile):
                return None
            self.current_profile_id = profile_id
            # 移除详细切换信息
            
            # 硬件配置切换后，清理服务池以获取新的机器码
            self.cleanup_dm_pool()
        
        # 确保服务池可用
        if not self.init_dm_pool():
            return None
        
        # 从池中获取服务
        dm_service = self.dm_pool.get_service()
        if not dm_service:
            return None
        
        try:
            # 注册服务
            reg_code = self.config.get_register_code()
            add_code = self.config.get_additional_code()
            ret_code, ret_msg = dm_service.register(reg_code, add_code)
            
            if ret_code != 1:
                self.log.error(f"大漠注册失败: {ret_msg}")
                return None
            
            # 获取信息
            version = dm_service.get_version()
            machine_code = dm_service.get_machine_code()
            mouse_pos = dm_service.get_cursor_pos()
        finally:
            # 归还服务到池中
            self.dm_pool.return_service(dm_service)
        
        # 记录完整的注册结果（包含鼠标位置）
        self.log.log_register_result(True, version, machine_code, mouse_pos)
        
        # 使用统一日志记录简洁信息
        self.log.log_simple_registration(machine_code)
        
        return {
            'version': version,
            'machine_code': machine_code,
            'mouse_pos': mouse_pos
        }
    
    def run_cycle(self) -> bool:
        """运行一轮注册"""
        self.log.log_section(f"开始运行循环 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        max_register_count = self.config.get_max_register_count()
        
        # 过滤掉已达到最大注册次数的机器码
        active_profiles = []
        for profile in self.profiles:
            machine_code = profile.get('machine_code', '未注册')
            if machine_code == '未注册':
                active_profiles.append(profile)
            else:
                count = self.machine_register_counts.get(machine_code, 0)
                if count < max_register_count:
                    active_profiles.append(profile)
                else:
                    self.log.info(f"机器码 {machine_code} 已达到最大注册次数({max_register_count})，跳过")
        
        if not active_profiles:
            self.log.info("所有机器码都已达到最大注册次数，本轮跳过")
            return False
        
        success_count = 0
        for i, profile in enumerate(active_profiles, 1):
            # 检查是否需要停止
            if not self.running:
                self.log.info("收到停止信号，中断当前循环")
                break
            
            self.log.log_separator()
            self.log.info(f"处理机器 {i}/{len(active_profiles)}")
            
            result = self.register_once(profile)
            
            if result:
                success_count += 1
                machine_code = result['machine_code']
                profile['machine_code'] = machine_code
                
                # 更新注册次数统计
                self.machine_register_counts[machine_code] = self.machine_register_counts.get(machine_code, 0) + 1
                
                self.profile_mgr.update_profile(profile['id'], profile)
        
        self.log.log_separator()
        self.log.info(f"本轮完成: 成功 {success_count}/{len(active_profiles)}")
        return success_count > 0
    
    def run(self):
        """运行注册循环"""
        if not self.initialize():
            self.log.error("初始化失败，无法启动")
            return
        
        self.running = True
        interval_minutes = self.config.get_interval_minutes()
        
        while self.running:
            # 运行一轮注册
            self.run_cycle()
            
            if not self.running:
                break
            
            # 等待指定时间
            next_time = datetime.now() + timedelta(minutes=interval_minutes)
            self.log.log_cycle_info(0, len(self.profiles), next_time)
            self.log.info(f"等待{interval_minutes}分钟后继续...")
            
            # 分段等待，以便可以响应停止信号
            wait_seconds = int(interval_minutes * 60)
            for _ in range(wait_seconds):
                if not self.running:
                    break
                time.sleep(1)
    
    def stop(self):
        """停止注册循环"""
        self.log.info("停止注册循环")
        self.running = False
    
    def cleanup(self):
        """清理资源"""
        if self.spoofer:
            self.spoofer.cleanup()
        self.cleanup_dm_pool()
        self.log.info("资源清理完成")