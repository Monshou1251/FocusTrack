from typing import Protocol

from app.core.logging.user_events import LogEvent


class LogPublisher(Protocol):
    async def publish(self, event: LogEvent) -> None: ...
