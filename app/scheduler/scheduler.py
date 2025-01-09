import heapq
from collections import deque
import threading
import time

class Scheduler:
    def __init__(self):
        self.resources = []
        self.task_queue = []  # priority queue
        self.failed_tasks = deque()  # queue for failed tasks
        self.lock = threading.Lock()
        self.running = True

    def add_resource(self, resource):
        with self.lock:
            self.resources.append(resource)

    def add_task(self, task):
        with self.lock:
            heapq.heappush(self.task_queue, task)

    def allocate_resources(self):
        with self.lock:
            if not self.task_queue:
                return

            task = heapq.heappop(self.task_queue)
            allocated = False

            for resource in self.resources:
                if resource.can_accommodate(task):
                    if resource.allocate(task):
                        task.status = "running"
                        allocated = True
                        break

            if not allocated:
                heapq.heappush(self.task_queue, task)

    def start(self):
        def run():
            while self.running:
                self.allocate_resources()
                time.sleep(1)  # Check every second

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.running = False 