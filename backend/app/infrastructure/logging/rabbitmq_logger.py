from app.core.interfaces import LogPublisher
from app.messaging.rabbitmq.publisher import publish_log

class RabbitMQLogPublisher(LogPublisher):
    def publish(self, log: dict) -> None:
        publish_log(log)
