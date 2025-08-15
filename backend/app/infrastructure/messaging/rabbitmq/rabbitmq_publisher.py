# app/core/logging/rabbitmq_log_publisher.py

import asyncio
import json
import logging
import os
import time

from aio_pika import Message, connect_robust

from app.core.config import settings
from app.core.logging.user_events import LogEvent
from app.domain.interfaces.log_publisher import LogPublisher

log_dir = "fallback_logs"
log_file = "fallback_logs.log"
log_path = os.path.join(log_dir, log_file)

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("log_publisher")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("Logger started, logs will be saved to %s", log_path)


class RabbitMQLogPublisher(LogPublisher):
    def __init__(self):
        self.url = settings.RABBITMQ_URL
        self.queue_name = settings.RABBITMQ_LOG_QUEUE
        self.connection = None
        self.channel = None
        self._next_retry_monotonic: float = 0.0

    async def _connect_with_throttle(self) -> bool:
        now = time.monotonic()
        if now < self._next_retry_monotonic:
            return False
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = await connect_robust(self.url, timeout=0.5)
                self.channel = await self.connection.channel()
                await self.channel.declare_queue(self.queue_name, durable=True)
            return True
        except Exception as exc:
            logger.warning(f"RabbitMQ connect failed: {exc}")
            self._next_retry_monotonic = now + 5.0
            return False

    async def _publish_now(self, log: LogEvent) -> None:
        try:
            if await self._connect_with_throttle():
                message = Message(
                    body=json.dumps(log.to_dict()).encode(), delivery_mode=2
                )
                await self.channel.default_exchange.publish(
                    message, routing_key=self.queue_name
                )
            else:
                logger.info(json.dumps(log.to_dict()))
        except Exception as exc:
            logger.warning(f"RabbitMQ publish failed: {exc}")
            self._next_retry_monotonic = time.monotonic() + 5.0
            logger.info(json.dumps(log.to_dict()))

    async def publish(self, log: LogEvent) -> None:
        asyncio.create_task(self._publish_now(log))
