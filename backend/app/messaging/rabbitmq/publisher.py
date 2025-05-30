import pika
import json
from app.core.config import settings

def publish_log(log_data: dict):
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_LOG_QUEUE, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=settings.RABBITMQ_LOG_QUEUE,
        body=json.dumps(log_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()
