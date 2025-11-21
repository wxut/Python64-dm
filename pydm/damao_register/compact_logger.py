"""精简日志记录器 - 只记录机器码注册信息"""
import os
import json
from datetime import datetime
from typing import Dict, Any

class CompactLogger:
    """精简日志记录器 - 覆盖式更新"""
    
    def __init__(self, log_file: str = "logs/machine_codes.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """加载现有数据"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"records": {}, "last_update": ""}
    
    def _save_data(self):
        """保存数据"""
        self.data["last_update"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def log_machine_code(self, machine_code: str, profile_id: int = None):
        """记录机器码注册信息（覆盖更新）"""
        if machine_code not in self.data["records"]:
            self.data["records"][machine_code] = {"count": 0, "profile_id": profile_id}
        
        self.data["records"][machine_code]["count"] += 1
        if profile_id:
            self.data["records"][machine_code]["profile_id"] = profile_id
        
        count = self.data["records"][machine_code]["count"]
        print(f"机器码{machine_code[:8]}...第{count}次注册")
        self._save_data()
    
    def get_summary(self) -> str:
        """获取注册摘要"""
        total = len(self.data["records"])
        total_count = sum(r["count"] for r in self.data["records"].values())
        return f"总计{total}个机器码，累计注册{total_count}次"

# 全局实例
_compact_logger = None

def get_compact_logger() -> CompactLogger:
    """获取精简日志记录器"""
    global _compact_logger
    if _compact_logger is None:
        _compact_logger = CompactLogger()
    return _compact_logger