import time
from base import TaskBase
from dag import DAG
from constants import SUBTASK_PREPARE
from subtask import SubTask


class Task(TaskBase):
    def __init__(
            self, task_id, name, status, description,
            worker, resource, STATEMACHINE, SUBTASK_DEPS,
    ):
        self.ctime = time.time()
        self.mtime = time.time()

        self.task_id = task_id
        self.name = name
        self.status = status
        self.description = description
        self.worker = worker
        self.resource = resource

        self.trim_task(STATEMACHINE, SUBTASK_DEPS)

    def trim_task(self, STATEMACHINE, SUBTASK_DEPS):
        deps, subtask2resource = self.gen_subtask_deps_and_relation(
            STATEMACHINE, SUBTASK_DEPS
        )
        self.topo = self.topo_sort(deps)
        self.subtasks = self.subtaskify(subtask2resource)

    def gen_subtask_deps_and_relation(self, STATEMACHINE, SUBTASK_DEPS):
        deps = {}
        subtask2resource = {}
        resource = self.resource

        origin_state = resource["origin_state"]
        target_state = resource["target_state"]
        for subtask_name in STATEMACHINE[origin_state][target_state]:  # noqa
            deps[subtask_name] = SUBTASK_DEPS[subtask_name]
            subtask2resource[subtask_name] = resource["resource_id"]

        return deps, subtask2resource

    def topo_sort(self, deps):
        dag = DAG()

        for u, vs in deps.items():
            if vs:
                for v in vs:
                    dag.add_edge(u, v)
            else:
                dag.add_edge(u)

        return dag.topo_sort()

    def subtaskify(self, subtask2resource):
        subtasks = {}

        for subtask_name in self.topo:
            resource_id = subtask2resource[subtask_name]
            subtask = SubTask(
                subtask_name,
                SUBTASK_PREPARE,
                "",
                self.resource["worker"],
                self.task_id,
                resource_id,
            )
            subtasks[subtask_name] = subtask.dumps()
        return subtasks
