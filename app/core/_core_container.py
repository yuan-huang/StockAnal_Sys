from dependency_injector import containers, providers
from app.core.database_providers import (
    get_mongo_client,
    get_mongo_database,
    get_redis_cache,
    get_redis_sessions,
    get_redis_tasks
)
from app.core.cache import Cache
from app.core.mongo_log_handler import MongoLogHandler

class CoreContainer(containers.DeclarativeContainer):
    # MongoDB 提供者
    mongo_client = providers.Singleton(get_mongo_client)
    mongo_database = providers.Singleton(get_mongo_database)
    
    # Redis 提供者
    redis_cache = providers.Singleton(get_redis_cache)
    redis_sessions = providers.Singleton(get_redis_sessions)
    redis_tasks = providers.Singleton(get_redis_tasks)
    
    # MongoDB日志处理器
    mongo_log_handler = providers.Singleton(MongoLogHandler)
    
    # 缓存服务
    cache = providers.Singleton(
        Cache,
        redis_client=redis_cache
    )
    
    # 分析容器 - 将在运行时动态配置
    analysis = providers.Dependency()