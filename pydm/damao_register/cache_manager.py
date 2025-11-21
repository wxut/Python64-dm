"""缓存管理模块"""
from typing import Dict, Any, Optional
import time


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, ttl: int = 300):  # 5分钟TTL
        self.hwid_cache: Dict[str, Dict] = {}
        self.register_cache: Dict[str, Dict] = {}
        self.ttl = ttl
    
    def get_cached_result(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """获取缓存的注册结果"""
        if profile_id in self.register_cache:
            cache_entry = self.register_cache[profile_id]
            if time.time() - cache_entry['timestamp'] < self.ttl:
                return cache_entry['data']
            else:
                del self.register_cache[profile_id]
        return None
    
    def cache_result(self, profile_id: str, result: Dict[str, Any]):
        """缓存注册结果"""
        self.register_cache[profile_id] = {
            'data': result,
            'timestamp': time.time()
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.hwid_cache.clear()
        self.register_cache.clear()