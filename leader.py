import time
import logging
from collections import defaultdict

from kombu import Producer
from base import Base
from utils import Singleton, get_uuid
from config import TASK_PREPARING, SUBTASK_PREPARE
from exceptions import WorkersNotSpecified, ResourcesError
from dag import DAG


class Leader(Base, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.producer = Producer(
            self.connection,
            exchange=self.task_exchange
        )
        self.resource_handlers = {}

    def add_handler(self, resource_type, handler):
        if resource_type in self.resource_handlers:
            logging.warning(
                "updating handler of resource type: %s" % resource_type
            )
        self.resource_handlers[resource_type] = handler

    def split(self, task):
        subtasks = self.subtaskfy(task)
        raise NotImplemented()

    def publish(self, task):
        for worker in task["workers"]:
            self.producer.publish(task, routing_key=worker)

    def subtaskfy(self, task):
        """
        split a task into multiple subtasks, each subtask contains a list of
        micro tasks, those micro tasks will be execting one by one in linear.
        but subtasks are parellel executing.

        NOTE: currently all micro tasks are executing one by one in linear.
        """
        dag = DAG()
        subtasks = []

        for u, vs in task["deps"].items():
            if vs:
                for v in vs:
                    dag.add_edge(u, v)
            else:
                dag.add_edge(u)
        for type in dag.topo_sort():
            subtasks.append({
                'type': type,
                'status': SUBTASK_PREPARE,
            })
        task["subtasks"] = subtasks


def task_deliver(
        resources,
        workers,
        deps,
        task_id=None,
        description="",
):
    if not workers:
        raise WorkersNotSpecified()

    if not isinstance(resources, list):
        raise ResourcesError("resources should be a list")

    task = {
        "task_id": task_id or get_uuid(),
        "description": description,
        "ctime": time.time(),
        "status": TASK_PREPARING,
        "workers": workers,
        "resources": resources,
        "deps": deps,
    }

    leader = Leader()
    leader.split(task)
    leader.publish(task)


if __name__ == "__main__":
    leader = Leader()

    def handler(*args, **kwargs):
        return []

    leader.add_handler("sayhi", handler)

    while True:
        resources = [
            {
                "type": "sleep",
                "hello": "world",
                "fuck": "you"
            },
            {
                "type": "eat",
            }
        ]
        deps = {
            "eat": ["sleep"],
            "sleep": [],
        }
        task_deliver(resources, ["worker1"], deps)
        time.sleep(3)
