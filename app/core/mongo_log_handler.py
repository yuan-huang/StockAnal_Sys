# app/core/mongo_log_handler.py
import logging
from .mongo_connector import get_mongo_db

class MongoLogHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)
        self.db = get_mongo_db()
        if self.db:
            self.log_collection = self.db.app_logs
        else:
            # Fallback to console if DB is not available
            print("WARNING: MongoDB not available for logging. Logs will not be saved.")
            self.log_collection = None

    def emit(self, record):
        if not self.log_collection:
            return

        try:
            log_entry = {
                'timestamp': self.formatTime(record, self.datefmt),
                'level': record.levelname,
                'message': self.format(record),
                'module': record.module,
                'funcName': record.funcName,
                'lineno': record.lineno,
            }
            # Insert the log entry into the collection
            self.log_collection.insert_one(log_entry)
        except Exception:
            # In case of logging failure, we don't want to crash the app.
            # We can just report the error to stderr.
            import sys
            sys.stderr.write("Failed to log to MongoDB.\\n")
            self.handleError(record)
