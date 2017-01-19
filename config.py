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
