# app/core/logging_config.py
"""
日志配置模块 - 配置应用程序的日志系统，包括MongoDB日志处理器
"""
import logging
import os
import sys
from pathlib import Path
from dependency_injector.wiring import Provide, inject
from ._core_container import CoreContainer

# 创建全局logger
logger = logging.getLogger('stock_analyzer')

class LoggingManager:
    """日志管理器"""
    
    @inject
    def __init__(self, mongo_log_handler=Provide[CoreContainer.mongo_log_handler]):
        self.mongo_log_handler = mongo_log_handler
        self.configured = False
    
    def setup_logging(self, log_level=None):
        """设置应用程序日志配置"""
        if self.configured:
            return
        
        # 获取日志级别
        if not log_level:
            log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # 配置根logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # 清除现有的处理器
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 1. 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # 2. 文件处理器
        log_file = os.getenv('LOG_FILE', 'data/logs/server.log')
        self._setup_file_handler(root_logger, log_file)
        
        # 3. MongoDB日志处理器
        if self.mongo_log_handler:
            mongo_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            self.mongo_log_handler.setFormatter(mongo_formatter)
            root_logger.addHandler(self.mongo_log_handler)
            logger.info("MongoDB日志处理器已添加")
        else:
            logger.warning("MongoDB日志处理器不可用")
        
        # 配置特定模块的日志级别
        self._configure_module_loggers()
        
        self.configured = True
        logger.info(f"日志系统初始化完成，级别: {log_level}")
    
    def _setup_file_handler(self, root_logger, log_file):
        """设置文件日志处理器"""
        try:
            # 确保日志目录存在
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建轮转文件处理器
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
            logger.info(f"文件日志处理器已配置: {log_file}")
        except Exception as e:
            logger.error(f"配置文件日志处理器失败: {e}")
    
    def _configure_module_loggers(self):
        """配置特定模块的日志级别"""
        # 设置第三方库的日志级别
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('pymongo').setLevel(logging.WARNING)
        logging.getLogger('redis').setLevel(logging.WARNING)
        
        # 设置应用模块的日志级别
        logging.getLogger('app').setLevel(logging.INFO)
        logging.getLogger('stock_analyzer').setLevel(logging.INFO)
    
    def get_logger(self, name):
        """获取指定名称的logger"""
        return logging.getLogger(name)
    
    def log_database_connection_status(self):
        """记录数据库连接状态"""
        try:
            from .database_providers import get_mongo_database, get_redis_cache
            
            # 检查MongoDB连接
            mongo_db = get_mongo_database()
            if mongo_db:
                collections = mongo_db.list_collection_names()
                logger.info(f"MongoDB连接正常，数据库: {mongo_db.name}，集合数: {len(collections)}")
            else:
                logger.error("MongoDB连接失败")
            
            # 检查Redis连接
            redis_client = get_redis_cache()
            if redis_client:
                redis_info = redis_client.info()
                logger.info(f"Redis连接正常，版本: {redis_info.get('redis_version', 'N/A')}")
            else:
                logger.error("Redis连接失败")
                
        except Exception as e:
            logger.error(f"检查数据库连接状态失败: {e}")

# 全局日志管理器实例
logging_manager = LoggingManager()

def setup_application_logging(log_level=None):
    """设置应用程序日志"""
    logging_manager.setup_logging(log_level)

def get_logger(name='stock_analyzer'):
    """获取logger实例"""
    return logging.getLogger(name)

def log_startup_info():
    """记录启动信息"""
    logger.info("="*50)
    logger.info("股票分析系统启动")
    logger.info("="*50)
    logging_manager.log_database_connection_status()

def log_shutdown_info():
    """记录关闭信息"""
    logger.info("股票分析系统关闭")
    logger.info("="*50) 