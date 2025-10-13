import os
from typing import List, Optional
from models import Task, TaskCreate
from utils import get_timestamp, generate_id

try:
    import pymongo
    MONGO_URI = os.getenv("MONGO_URI", None)
except ImportError:
    pymongo = None
    MONGO_URI = None

import json

DB_NAME = "taskdb"
COLLECTION_NAME = "tasks"
JSON_PATH = "tasks.json"

class TaskDataHandler:
    def __init__(self):
        self.use_mongo = pymongo and MONGO_URI
        if self.use_mongo:
            self.client = pymongo.MongoClient(MONGO_URI)
            self.collection = self.client[DB_NAME][COLLECTION_NAME]
        else:
            if not os.path.exists(JSON_PATH):
                with open(JSON_PATH, "w") as f:
                    json.dump([], f)

    def create_task(self, data: TaskCreate) -> Task:
        task = Task(
            id=generate_id(),
            title=data.title,
            description=data.description,
            is_completed=False,
            created_at=get_timestamp()
        )
        if self.use_mongo:
            self.collection.insert_one(task.dict())
        else:
            tasks = self._read_file()
            tasks.append(task.dict())
            self._write_file(tasks)
        return task

    def get_tasks(self, is_completed: Optional[bool]=None) -> List[Task]:
        if self.use_mongo:
            query = {}
            if is_completed is not None:
                query['is_completed'] = is_completed
            tasks = list(self.collection.find(query, {"_id": 0}))
        else:
            tasks = self._read_file()
            if is_completed is not None:
                tasks = [t for t in tasks if t["is_completed"] == is_completed]
        return [Task(**t) for t in tasks]

    def mark_completed(self, task_id: str) -> Optional[Task]:
        if self.use_mongo:
            res = self.collection.find_one_and_update(
                {"id": task_id},
                {"$set": {"is_completed": True}},
                return_document=pymongo.ReturnDocument.AFTER
            )
            if res:
                res.pop("_id", None)
                return Task(**res)
        else:
            tasks = self._read_file()
            for t in tasks:
                if t["id"] == task_id:
                    t["is_completed"] = True
                    self._write_file(tasks)
                    return Task(**t)
        return None

    def delete_task(self, task_id: str) -> bool:
        if self.use_mongo:
            result = self.collection.delete_one({"id": task_id})
            return result.deleted_count > 0
        else:
            tasks = self._read_file()
            orig_len = len(tasks)
            tasks = [t for t in tasks if t["id"] != task_id]
            self._write_file(tasks)
            return len(tasks) < orig_len

    def _read_file(self):
        with open(JSON_PATH, "r") as f:
            return json.load(f)

    def _write_file(self, tasks):
        with open(JSON_PATH, "w") as f:
            json.dump(tasks, f, default=str)
