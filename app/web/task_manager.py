# app/web/task_manager.py
import uuid
import threading
import time
from datetime import datetime
import logging
from enum import Enum
import redis
import json
from app.core.connections import REDIS_URL_TASKS, IS_DOCKER # Import centralized URL

class TaskStatus(str, Enum):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.redis_client = redis.from_url(REDIS_URL_TASKS, decode_responses=True) # Use centralized URL
            self.redis_client.ping()
            self.logger.info(f"Successfully connected to Redis for TaskManager. Docker mode: {IS_DOCKER}")
        except redis.exceptions.ConnectionError as e:
            self.logger.error(f"FATAL: Could not connect to Redis for TaskManager. Tasks will not be operational. Error: {e}")
            self.redis_client = None

    def _serialize(self, data):
        if data is None:
            return None
        return json.dumps(data)

    def _deserialize(self, data):
        if data is None:
            return None
        return json.loads(data)

    def _generate_task_id(self):
        return str(uuid.uuid4())

    def create_task(self, name, params=None):
        if not self.redis_client:
            return None
            
        task_id = self._generate_task_id()
        now = datetime.now()
        task = {
            'id': task_id,
            'name': name,
            'status': TaskStatus.PENDING.value,
            'progress': 0,
            'result': self._serialize(None),
            'error': self._serialize(None),
            'params': self._serialize(params or {}),
            'created_at': now.isoformat(),
            'updated_at': now.isoformat(),
        }
        
        task_key = f"task:{task_id}"
        with self.redis_client.pipeline() as pipe:
            pipe.hset(task_key, mapping=task)
            # Use timestamp as score for sorting
            pipe.zadd('tasks_sorted_by_time', {task_id: now.timestamp()})
            pipe.execute()
            
        self.logger.info(f"Task created in Redis: {task_id} ({name})")
        
        # Return a deserialized version for immediate use
        task['result'] = None
        task['error'] = None
        task['params'] = params or {}
        return task

    def get_task(self, task_id):
        if not self.redis_client:
            return None

        task_key = f"task:{task_id}"
        task_data = self.redis_client.hgetall(task_key)

        if not task_data:
            return None
            
        # Deserialize complex fields
        task_data['progress'] = int(task_data.get('progress', 0))
        task_data['result'] = self._deserialize(task_data.get('result'))
        task_data['error'] = self._deserialize(task_data.get('error'))
        task_data['params'] = self._deserialize(task_data.get('params'))
        
        return task_data

    def get_all_tasks(self):
        if not self.redis_client:
            return []

        # Get all task IDs, newest first
        task_ids = self.redis_client.zrevrange('tasks_sorted_by_time', 0, -1)
        
        tasks = []
        with self.redis_client.pipeline() as pipe:
            for task_id in task_ids:
                pipe.hgetall(f"task:{task_id}")
            task_data_list = pipe.execute()

        for task_data in task_data_list:
            if task_data:
                # Deserialize complex fields
                task_data['progress'] = int(task_data.get('progress', 0))
                task_data['result'] = self._deserialize(task_data.get('result'))
                task_data['error'] = self._deserialize(task_data.get('error'))
                task_data['params'] = self._deserialize(task_data.get('params'))
                tasks.append(task_data)
                
        return tasks

    def update_task(self, task_id, status=None, progress=None, result=None, error=None):
        if not self.redis_client:
            return None

        task_key = f"task:{task_id}"
        if not self.redis_client.exists(task_key):
            self.logger.warning(f"Attempted to update non-existent task: {task_id}")
            return None

        update_data = {'updated_at': datetime.now().isoformat()}
        if status:
            update_data['status'] = status.value if isinstance(status, Enum) else status
        if progress is not None:
            update_data['progress'] = progress
        if result is not None:
            update_data['result'] = self._serialize(result)
        if error is not None:
            update_data['error'] = self._serialize(error)
        
        self.redis_client.hset(task_key, mapping=update_data)
        return self.get_task(task_id)

    def delete_task(self, task_id):
        if not self.redis_client:
            return False

        task_key = f"task:{task_id}"
        with self.redis_client.pipeline() as pipe:
            pipe.delete(task_key)
            pipe.zrem('tasks_sorted_by_time', task_id)
            results = pipe.execute()
        
        deleted_count = results[0]
        if deleted_count > 0:
            self.logger.info(f"Task deleted from Redis: {task_id}")
            return True
        return False

    def _clean_old_tasks(self):
        """Clean up old, completed/failed tasks from Redis."""
        if not self.redis_client:
            return

        # Clean tasks older than 1 hour (3600 seconds)
        cutoff_timestamp = time.time() - 3600
        
        # Find tasks with an updated_at timestamp older than the cutoff
        # This is complex with Hashes. A simpler approach is to use a second sorted set.
        # For now, let's iterate, but this is inefficient for large numbers of tasks.
        task_ids = self.redis_client.zrange('tasks_sorted_by_time', 0, -1)
        
        to_delete = []
        for task_id in task_ids:
            task_status, updated_at_iso = self.redis_client.hmget(f"task:{task_id}", ['status', 'updated_at'])
            if task_status in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value]:
                try:
                    updated_at = datetime.fromisoformat(updated_at_iso)
                    if updated_at.timestamp() < cutoff_timestamp:
                        to_delete.append(task_id)
                except (ValueError, TypeError):
                    # Invalid timestamp, mark for deletion
                    to_delete.append(task_id)
        
        if to_delete:
            for task_id in to_delete:
                self.delete_task(task_id)
            self.logger.info(f"Cleaned up {len(to_delete)} old tasks from Redis.")

    def _run_cleaner(self):
        """Periodically run the task cleaner."""
        while True:
            try:
                self._clean_old_tasks()
            except Exception as e:
                self.logger.error(f"Error in Redis task cleaner thread: {e}", exc_info=True)
            time.sleep(600)  # Run every 10 minutes

    def start_cleaner_thread(self):
        if not self.redis_client:
            self.logger.warning("Redis client not available. Task cleaner thread not started.")
            return
            
        cleaner_thread = threading.Thread(target=self._run_cleaner, daemon=True)
        cleaner_thread.start()
        self.logger.info("Redis-based Task cleaner thread started.")

# Singleton instance
task_manager = TaskManager()
