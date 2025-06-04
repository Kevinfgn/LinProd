import time
from collections import deque

class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration  # en segundos o ciclos
        self.queue = deque()
        self.current_product = None
        self.remaining_time = 0
        self.busy = False

    def enqueue_product(self, product):
        self.queue.append(product)

    def process(self):
        if self.busy:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                completed = self.current_product
                self.current_product = None
                self.busy = False
                return completed
        elif self.queue:
            self.current_product = self.queue.popleft()
            self.busy = True
            self.remaining_time = self.duration
        return None

    def status(self):
        return {
            "task": self.name,
            "busy": self.busy,
            "queue_length": len(self.queue),
            "current_product": self.current_product.id if self.current_product else None
        }


class Process:
    def __init__(self, name, is_start=False, is_end=False):
        self.name = name
        self.tasks = []
        self.next_process = None
        self.is_start = is_start
        self.is_end = is_end

    def add_task(self, task: Task):
        self.tasks.append(task)

    def set_next_process(self, process):
        self.next_process = process

    def enqueue_product(self, product):
        if self.tasks:
            self.tasks[0].enqueue_product(product)

    def run_cycle(self):
        for i, task in enumerate(self.tasks):
            result = task.process()
            if result and i < len(self.tasks) - 1:
                self.tasks[i + 1].enqueue_product(result)
            elif result and self.next_process:
                self.next_process.enqueue_product(result)
            elif result and self.is_end:
                result.completed = True
                result.exit_time = time.time()
                return result  # producto completado
        return None

    def status(self):
        return {
            "process": self.name,
            "tasks": [task.status() for task in self.tasks]
        }
