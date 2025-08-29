# app/core/cache.py
import redis
import json
from datetime import datetime, time
import os
import threading
import logging
from .connections import REDIS_URL_CACHE, IS_DOCKER # Import centralized URL

# USE_REDIS_CACHE is still useful to allow disabling Redis for specific debugging.
USE_REDIS_CACHE = os.getenv('USE_REDIS_CACHE', 'True').lower() == 'true'

class CacheManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # 防止重复初始化
            self.logger = logging.getLogger(__name__)
            if USE_REDIS_CACHE:
                try:
                    self.redis_client = redis.from_url(REDIS_URL_CACHE) # Use centralized URL
                    self.redis_client.ping()
                    self.cache_type = 'redis'
                    self.logger.info(f"Successfully connected to Redis for CacheManager. Docker mode: {IS_DOCKER}")
                except redis.exceptions.ConnectionError as e:
                    self.logger.warning(f"Could not connect to Redis for Cache. Falling back to in-memory. Error: {e}")
                    self.in_memory_cache = {}
                    self.cache_type = 'memory'
            else:
                self.in_memory_cache = {}
                self.cache_type = 'memory'
                self.logger.info("Redis cache is disabled. Using in-memory cache.")
            self.initialized = True
            self.last_cleared_date = datetime.now().date()

    def get(self, key):
        self._clear_cache_if_new_day()
        if self.cache_type == 'redis':
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        else:
            return self.in_memory_cache.get(key)

    def set(self, key, value, ttl=3600): # 默认1小时过期
        self._clear_cache_if_new_day()
        if self.cache_type == 'redis':
            self.redis_client.set(key, json.dumps(value), ex=ttl)
        else:
            self.in_memory_cache[key] = value

    def _clear_cache_if_new_day(self):
        """
        检查是否是新的交易日，如果是，则清空缓存。
        收盘时间定义为16:00。
        """
        now = datetime.now()
        today = now.date()
        
        # 如果当前日期大于上次清理日期，则执行清理
        if today > self.last_cleared_date:
            # A股收盘时间为15:00，我们可以在16:00后清理，确保数据已固化
            market_close_time = time(16, 0)
            
            if now.time() > market_close_time:
                print(f"New day detected ({today}). Clearing all cache.")
                self.clear_all()
                self.last_cleared_date = today

    def clear_all(self):
        if self.cache_type == 'redis':
            self.redis_client.flushdb()
            print("Redis cache cleared.")
        else:
            self.in_memory_cache.clear()
            print("In-memory cache cleared.")

# 全局缓存实例
cache_manager = CacheManager()

def get_cache():
    return cache_manager
