# app/core/cache.py
import json
from datetime import datetime
import os
import logging
import redis

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self, redis_client=None):
        """
        初始化缓存
        Args:
            redis_client: Redis客户端实例，通过依赖注入提供
        """
        self.logger = logging.getLogger(__name__)
        self.redis_client = redis_client
        
        # 检查是否启用Redis缓存
        use_redis = os.getenv('USE_REDIS_CACHE', 'False').lower() == 'true'
        
        if use_redis and redis_client:
            try:
                redis_client.ping()
                self.cache_type = 'redis'
                self.logger.info("缓存初始化成功 - 使用Redis")
            except Exception as e:
                self.logger.warning(f"Redis连接失败，使用内存缓存: {e}")
                self.cache_type = 'memory'
                self._memory_cache = {}
        else:
            self.cache_type = 'memory'
            self._memory_cache = {}
            self.logger.info("缓存初始化成功 - 使用内存缓存")

    def get(self, key):
        """获取缓存值"""
        try:
            if self.cache_type == 'redis' and self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                return self._memory_cache.get(key)
        except Exception as e:
            self.logger.error(f"获取缓存失败 {key}: {e}")
        return None

    def set(self, key, value, expire=3600):
        """设置缓存值"""
        try:
            if self.cache_type == 'redis' and self.redis_client:
                self.redis_client.setex(key, expire, json.dumps(value, ensure_ascii=False))
            else:
                # 内存缓存暂不处理过期时间
                self._memory_cache[key] = value
        except Exception as e:
            self.logger.error(f"设置缓存失败 {key}: {e}")

    def delete(self, key):
        """删除缓存"""
        try:
            if self.cache_type == 'redis' and self.redis_client:
                self.redis_client.delete(key)
            else:
                self._memory_cache.pop(key, None)
        except Exception as e:
            self.logger.error(f"删除缓存失败 {key}: {e}")

    def clear(self):
        """清空所有缓存"""
        try:
            if self.cache_type == 'redis' and self.redis_client:
                self.redis_client.flushdb()
            else:
                self._memory_cache.clear()
        except Exception as e:
            self.logger.error(f"清空缓存失败: {e}")

    def exists(self, key):
        """检查缓存是否存在"""
        try:
            if self.cache_type == 'redis' and self.redis_client:
                return self.redis_client.exists(key)
            else:
                return key in self._memory_cache
        except Exception as e:
            self.logger.error(f"检查缓存存在性失败 {key}: {e}")
            return False

    def get_cache_info(self):
        """获取缓存信息"""
        info = {
            'type': self.cache_type,
            'status': 'connected' if self.cache_type == 'redis' else 'memory'
        }
        
        try:
            if self.cache_type == 'redis' and self.redis_client:
                info['size'] = self.redis_client.dbsize()
                redis_info = self.redis_client.info()
                info['memory_usage'] = redis_info.get('used_memory_human', 'N/A')
            else:
                info['size'] = len(self._memory_cache)
                info['memory_usage'] = 'N/A'
        except Exception as e:
            self.logger.error(f"获取缓存信息失败: {e}")
            info['error'] = str(e)
        
        return info