import time

from kombu import Producer
from base import Base


class Leader(Base):
    def __init__(self):
        super().__init__()
        self.producer = Producer(
            self.connection,
            exchange=self.task_exchange
        )

    def publish(self, msg, routing_key=None):
        self.producer.publish(msg, routing_key=routing_key)


if __name__ == "__main__":
    leader = Leader()

    while True:
        leader.publish(
            {
                "hello": "world",
                "time": time.time(),
            },
            "consumer1",
        )
        time.sleep(3)
