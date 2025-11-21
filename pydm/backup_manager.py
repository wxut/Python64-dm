"""备份管理器 - 优化前自动备份文件"""
import os
import shutil
from datetime import datetime

class BackupManager:
    def __init__(self, backup_dir="backup"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup_file(self, file_path):
        """备份单个文件"""
        if not os.path.exists(file_path):
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_name = f"{filename}.{timestamp}.bak"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        shutil.copy2(file_path, backup_path)
        print(f"[BACKUP] {file_path} -> {backup_path}")
        return backup_path
    
    def restore_file(self, backup_path, original_path):
        """恢复文件"""
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            print(f"[RESTORE] {backup_path} -> {original_path}")
            return True
        return False

# 全局备份管理器
backup_mgr = BackupManager()