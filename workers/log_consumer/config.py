import os

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost/")
RABBITMQ_LOG_QUEUE = os.environ.get("RABBITMQ_LOG_QUEUE", "log_queue2")