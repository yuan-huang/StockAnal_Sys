# app/core/mongo_log_handler.py
import logging
from datetime import datetime
try:
    from .database_providers import get_mongo_database
except ImportError:
    from app.core.database_providers import get_mongo_database

class MongoLogHandler(logging.Handler):
    """MongoDB日志处理器 - 将日志保存到MongoDB中"""
    
    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)
        self.db = get_mongo_database()
        if self.db:
            self.log_collection = self.db.app_logs
            print("MongoDB日志处理器初始化成功")
        else:
            # 如果数据库不可用，回退到控制台
            print("警告: MongoDB不可用于日志记录。日志将不会被保存。")
            self.log_collection = None

    def emit(self, record):
        """发送日志记录到MongoDB"""
        if not self.log_collection:
            return

        try:
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created),
                'level': record.levelname,
                'message': self.format(record),
                'module': record.module,
                'funcName': record.funcName,
                'lineno': record.lineno,
                'pathname': record.pathname,
                'process': record.process,
                'thread': record.thread,
                'created': record.created
            }
            # 将日志条目插入到集合中
            self.log_collection.insert_one(log_entry)
        except Exception as e:
            # 如果日志记录失败，我们不想让应用崩溃
            # 我们可以将错误报告到stderr
            import sys
            sys.stderr.write(f"保存日志到MongoDB失败: {e}\n")
            self.handleError(record)
