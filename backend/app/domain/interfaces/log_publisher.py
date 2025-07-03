from typing import Protocol

from app.core.logging.events import LogEvent


class LogPublisher(Protocol):
    async def publish(self, event: LogEvent) -> None: ...
