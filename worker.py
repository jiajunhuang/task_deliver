from base import Base
from kombu import Consumer, Queue


class Worker(Base):
    def __init__(self):
        super().__init__()
        self.task_queue = Queue(
            'consumer1', self.task_exchange, routing_key='consumer1'
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
    worker = Worker()
    worker.consume()
