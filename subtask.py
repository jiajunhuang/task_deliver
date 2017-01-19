from base import TaskBase


class SubTask(TaskBase):
    def __init__(
            self, name: str, status: str,
            description: str, worker: str, task_id: str,
            resource_id: str
    ):
        self.name = name
        self.status = status
        self.description = description
        self.worker = worker
        self.task_id = task_id
        self.resource_id = resource_id
