from kombu import Connection, Exchange


class Base:
    def __init__(self):
        self._connection = Connection("mongodb://127.0.0.1:27017")
        self._connection.connect()
        self.task_exchange = Exchange("tasks", type="direct")

    @property
    def connection(self):
        return self._connection
