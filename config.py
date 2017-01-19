from pymongo import MongoClient

mongodb = MongoClient()

MONGODB_CONNECTION = "mongodb://127.0.0.1:27017"

TASK_PREPARING = "preparing"
TASK_PROCESSING = "processing"
TASK_SUCCEED = "succeed"
TASK_FAILED = "failed"

SUBTASK_PREPARE = "subtask_preparing"
SUBTASK_PROCESSING = "processing"
SUBTASK_SUCCEED = "succeed"
SUBTASK_FAILED = "failed"

STATEMACHINE = {
    "wake": {
        "sleep": ["TASK_EAT", "TASK_WASH", "TASK_SLEEP"]
    },
    "hungry": {
        "full": ["TASK_EAT"]
    }
}

SUBTASK_DEPS = {
    "TASK_EAT": ["TASK_SLEEP"],
    "TASK_WASH": ["TASK_SLEEP"],
    "TASK_SLEEP": [],
}

SUBTASK_HANDLER = {
    "TASK_EAT": lambda: print("executing TASK_EAT..."),
    "TASK_WASH": lambda: print("executing TASK_WASH..."),
    "TASK_SLEEP": lambda: print("executing TASK_SLEEP..."),
}
