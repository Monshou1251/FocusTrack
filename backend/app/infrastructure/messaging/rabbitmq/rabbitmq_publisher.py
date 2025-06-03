# app/core/logging/rabbitmq_log_publisher.py

from aio_pika import connect_robust, Message
import json
from app.core.config import settings
import logging
from app.core.interfaces import LogPublisher
import os

log_dir = "fallback_logs"
log_file = "fallback_logs.log"
log_path = os.path.join(log_dir, log_file)

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("log_publisher")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("Logger started, logs will be saved to %s", log_path)


class RabbitMQLogPublisher(LogPublisher):
    def __init__(self):
        self.url = settings.RABBITMQ_URL
        self.queue_name = settings.RABBITMQ_LOG_QUEUE
        self.connection = None
        self.channel = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, log: dict) -> None:
        try:
            await self.connect()
            message = Message(body=json.dumps(log.to_dict()).encode(), delivery_mode=2)
            await self.channel.default_exchange.publish(message, routing_key=self.queue_name)
            print("RabbitMQ available, message sent")
        except Exception as e:
            logger.warning(f"RabbitMQ unavailable: {e}")
            print(f"RabbitMQ unavailable: {e}")
            logger.info(json.dumps(log.to_dict())) 
