# app/core/mongo_connector.py
import os
from .connections import MONGO_URI
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoConnector:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnector, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.logger = logging.getLogger(__name__)
        # MONGO_URI is now sourced from the centralized connections module
        db_name = MONGO_URI.split('/')[-1]

        try:
            self.logger.info(f"Connecting to MongoDB...")
            self._client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self._client.admin.command('ismaster')
            self._db = self._client[db_name]
            self.logger.info("Successfully connected to MongoDB.")
        except ConnectionFailure as e:
            self.logger.error(f"FATAL: Could not connect to MongoDB. URI: {MONGO_URI} Error: {e}")
            self._client = None
            self._db = None

    def get_db(self):
        return self._db

# Singleton instance
mongo_connector = MongoConnector()

def get_mongo_db():
    return mongo_connector.get_db()
