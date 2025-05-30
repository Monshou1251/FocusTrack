import json
import pika
from app.core.config import settings
from datetime import datetime, timezone
from pathlib import Path
import os


# Путь до app/logs/logs.jsonl
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "logs.jsonl")

def callback(ch, method, properties, body):
    log = json.loads(body)
    
    print(f"[{datetime.now().isoformat()}] Log received: {log}")
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **log
        }) + "\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_log_worker():
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_LOG_QUEUE, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.RABBITMQ_LOG_QUEUE, on_message_callback=callback)

    print("[*] Waiting for logs...")
    channel.start_consuming()

if __name__ == "__main__":
    print(f"Writing to log file: {LOG_PATH}")

    start_log_worker()
