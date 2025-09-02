# app/core/database_providers.py
import os
import logging
import redis
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

def get_mongo_client():
    """获取MongoDB客户端"""
    host = os.getenv('MONGODB_HOST', 'localhost')
    port = int(os.getenv('MONGODB_PORT', 27017))
    db_name = os.getenv('MONGODB_DATABASE', 'tradingagents')
    username = os.getenv('MONGODB_USERNAME', '')
    password = os.getenv('MONGODB_PASSWORD', '')
    
    # 构建连接URI
    if username and password:
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
    else:
        uri = f"mongodb://{host}:{port}/{db_name}"
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # 测试连接
        client.admin.command('ping')
        logger.info(f"MongoDB连接成功: {host}:{port}/{db_name}")
        return client
    except Exception as e:
        logger.error(f"MongoDB连接失败: {e}")
        return None

def get_mongo_database():
    """获取MongoDB数据库实例"""
    client = get_mongo_client()
    if client:
        db_name = os.getenv('MONGO_DB_NAME', 'tradingagents')
        return client[db_name]
    return None

def get_redis_client(db=0):
    """获取Redis客户端"""
    host = os.getenv('REDIS_HOST', 'localhost')
    port = int(os.getenv('REDIS_PORT', 6379))
    password = os.getenv('REDIS_PASS', '')
    
    try:
        if password:
            client = redis.Redis(
                host=host,
                port=port,
                password=password,
                db=db,
                decode_responses=True
            )
        else:
            client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True
            )
        
        # 测试连接
        client.ping()
        logger.info(f"Redis连接成功: {host}:{port}/db{db}")
        return client
    except Exception as e:
        logger.error(f"Redis连接失败: {e}")
        return None

def get_redis_cache():
    """获取Redis缓存客户端 (db=0)"""
    return get_redis_client(0)

def get_redis_sessions():
    """获取Redis会话客户端 (db=1)"""
    return get_redis_client(1)

def get_redis_tasks():
    """获取Redis任务客户端 (db=2)"""
    return get_redis_client(2) 