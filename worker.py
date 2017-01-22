import logging

from base import Base
from kombu import Consumer, Queue
from utils import Singleton
from config import HANDLERS_MAPPER, SUBTASK_FAILED, SUBTASK_SUCCEED
from exceptions import HandlerNotFound


class Worker(Base, metaclass=Singleton):
    def __init__(self, worker_name, routing_key):
        super().__init__()
        self.task_queue = Queue(
            worker_name, self.task_exchange, routing_key=routing_key
        )
        self._consumer = Consumer(
            self.connection,
            queues=[self.task_queue],
            callbacks=[self.process],
        )
        self._consumer.consume()

    def process(self, subtask, message):
        import time
        time.sleep(3)
        handler = HANDLERS_MAPPER.get(subtask["type"])
        if not handler:
            raise HandlerNotFound("handler not found of subtask: %s" % subtask)
        try:
            handler()
            self.report_subtask_status(subtask["task_id"], SUBTASK_SUCCEED, "")
        except Exception as e:
            logging.error("executing subtask(%s) failed" % subtask)
            self.report_subtask_status(
                subtask["task_id"], SUBTASK_FAILED, str(e)
            )

    def report_subtask_status(self, task_id, status, description):
        pass

    def consume(self):
        while True:
            self.connection.drain_events()


if __name__ == "__main__":
    worker = Worker('worker1', 'worker1')
    worker.consume()
