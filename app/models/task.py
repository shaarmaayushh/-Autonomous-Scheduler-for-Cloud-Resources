import time
from datetime import datetime
import json

class Task:
    def __init__(self, id, priority, deadline, required_cpu, required_memory):
        self.id = id
        self.priority = priority
        self.deadline = time.time() + deadline  # deadline in seconds from now
        self.required_cpu = required_cpu
        self.required_memory = required_memory
        self.status = "pending"
        self.created_at = time.time()
        self.dependencies = []
        self.retry_count = 0
        self.max_retries = 3
        self.tags = []
        self.group_id = None

    def __lt__(self, other):
        # For priority queue comparison
        return self.priority < other.priority 

    def get_duration(self):
        if self.started_at is None:
            return 0
        end_time = self.completed_at or time.time()
        return end_time - self.started_at

    def get_time_until_deadline(self):
        return self.deadline - time.time()

    def is_overdue(self):
        return time.time() > self.deadline 

    def add_dependency(self, task):
        if task not in self.dependencies:
            self.dependencies.append(task)

    def can_start(self):
        return all(dep.status == "completed" for dep in self.dependencies)

    def to_dict(self):
        return {
            "id": self.id,
            "priority": self.priority,
            "deadline": self.deadline,
            "required_cpu": self.required_cpu,
            "required_memory": self.required_memory,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        task = cls(
            id=data["id"],
            priority=data["priority"],
            deadline=data["deadline"],
            required_cpu=data["required_cpu"],
            required_memory=data["required_memory"]
        )
        task.status = data["status"]
        task.created_at = data["created_at"]
        task.started_at = data["started_at"]
        task.completed_at = data["completed_at"]
        return task 