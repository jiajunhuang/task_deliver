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

# ##### deps resolver
from resolvers.eat import eat
from resolvers.sleep import sleep
RESOLVER_MAPPER = {
    "eat": eat,
    "sleep": sleep,
}


# #### handlers
from handlers.say_hi import say_hi

HANDLERS_MAPPER = {
    "say_hi": say_hi,
}
