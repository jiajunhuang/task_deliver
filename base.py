import json

from kombu import Connection, Exchange
from config import MONGODB_CONNECTION


class Base:
    def __init__(self):
        self._connection = Connection(MONGODB_CONNECTION)
        self._connection.connect()
        self.task_exchange = Exchange("tasks", type="direct")

    @property
    def connection(self):
        return self._connection


class TaskBase:
    def jsonify(self):
        return json.dumps(self.__dict__)

    def dumps(self):
        return self.__dict__
