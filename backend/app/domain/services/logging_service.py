from datetime import datetime, timezone
from app.core.interfaces import LogPublisher

async def log_auth(
    event: str,
    log_publisher: LogPublisher,
    email: str,
    success: bool,
    ip: str,
):
    await log_publisher.publish({
        "event": event,
        "email": email,
        "success": success,
        "ip": ip,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
