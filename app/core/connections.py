# app/core/connections.py
import os

# This logic determines the correct hostname for services
# based on the execution environment (local machine vs. Docker).
IS_DOCKER = os.getenv('RUNNING_IN_DOCKER', 'false').lower() == 'true'

DB_HOST = "mongodb" if IS_DOCKER else "localhost"
REDIS_HOST = "redis" if IS_DOCKER else "localhost"

# Read credentials from environment variables, with sensible defaults
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS", "tradingagents123")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "tradingagents")

REDIS_PASS = os.getenv("REDIS_PASS", "tradingagents123")

# Construct the full connection URIs
# These will now be the single source of truth for connection strings.
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{DB_HOST}:27017/{MONGO_DB_NAME}"
# We define URLs for each database we use to keep it clean.
REDIS_URL_CACHE = f"redis://:{REDIS_PASS}@{REDIS_HOST}:6379/0"
REDIS_URL_TASKS = f"redis://:{REDIS_PASS}@{REDIS_HOST}:6379/1"
REDIS_URL_SESSIONS = f"redis://:{REDIS_PASS}@{REDIS_HOST}:6379/2"
