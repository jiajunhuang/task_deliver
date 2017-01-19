import time
import logging

from kombu import Producer
from base import Base
from utils import Singleton, get_uuid
from exceptions import WorkerNotSpecified, ResourcesError, SubTaskFailed
from dag import DAG
from config import (
    TASK_PREPARING,
    TASK_FAILED,
    TASK_SUCCEED,
    SUBTASK_PREPARE,
    SUBTASK_FAILED,
    RESOLVER_MAPPER,
)


class Leader(Base, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.producer = Producer(
            self.connection,
            exchange=self.task_exchange
        )

    def publish(self, task):
        self.resolve_deps(task)
        self.subtaskfy(task)
        try:
            next_subtask = self.next_subtask(task)
            logging.debug("next subtask: %s" % next_subtask)
            if next_subtask is None:
                self.update_task_status(TASK_SUCCEED, "")
            else:
                self.producer.publish(next_subtask, routing_key=task["worker"])
        except SubTaskFailed:
            logging.error("subtask in worker %s had failed")
            self.update_task_status(
                TASK_FAILED, "task failed due to subtask"
            )

    def update_task_status(self, task, status, description):
        task["status"], task["description"] = status, description

    def next_subtask(self, task):
        subtasks = task["subtasks"]
        for subtask in subtasks:
            if subtask["status"] == SUBTASK_PREPARE:
                return subtask
            elif subtask["status"] == SUBTASK_FAILED:
                raise SubTaskFailed()
        return None

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
                "type": type,
                "status": SUBTASK_PREPARE,
            })
        task["subtasks"] = subtasks

    def resolve_deps(self, task):
        deps = {}
        for resource in task["resources"]:
            deps.update(RESOLVER_MAPPER[resource["type"]](task))
        task["deps"] = deps


def task_deliver(
        resources,
        worker,
        task_id=None,
        description="",
):
    if not worker:
        raise WorkerNotSpecified()

    if not isinstance(resources, list):
        raise ResourcesError("resources should be a list")

    task = {
        "task_id": task_id or get_uuid(),
        "description": description,
        "ctime": time.time(),
        "status": TASK_PREPARING,
        "worker": worker,
        "resources": resources,
    }

    leader = Leader()
    leader.publish(task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    leader = Leader()

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
        task_deliver(resources, "worker1")
        time.sleep(3)
