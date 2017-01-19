import uuid

from constants import TASK_PREPARING
from task import Task
from config import STATEMACHINE, SUBTASK_DEPS


resource_uuid1 = str(uuid.uuid4())
resource_uuid2 = str(uuid.uuid4())
resource = {
    "resource_id": resource_uuid1,
    "worker": "worker1",
    "time": "10hours",
    "origin_state": "wake",
    "target_state": "sleep",
}

t = Task(
    str(uuid.uuid4()), "sleep after eat",
    TASK_PREPARING, "", "worker1", resource,
    STATEMACHINE, SUBTASK_DEPS,
)
print(t.jsonify())
