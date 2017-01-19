from base import Base
from kombu import Consumer, Queue
from utils import Singleton


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

    def process(self, body, message):
        print(body, message)

    def consume(self):
        while True:
            self.connection.drain_events()


if __name__ == "__main__":
    worker = Worker('worker1', 'worker1')
    worker.consume()
