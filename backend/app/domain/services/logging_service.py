from app.core.logging.events import (
    OAuthLoginAttemptLog,
    UserLoginAttemptLog,
    UserRegistrationAttemptLog,
)
from app.domain.interfaces.log_publisher import LogPublisher


async def log_auth_attempt(
    log_publisher: LogPublisher,
    email: str,
    success: bool,
    ip: str,
    error: str | None = None,
):
    event = UserLoginAttemptLog(email=email, success=success, ip=ip, error=error)
    await log_publisher.publish(event)


async def log_registration_attempt(
    log_publisher: LogPublisher,
    email: str,
    success: bool,
    ip: str,
    error: str | None = None,
):
    event = UserRegistrationAttemptLog(email=email, success=success, ip=ip, error=error)
    await log_publisher.publish(event)


async def log_oauth_attempt(
    log_publisher: LogPublisher,
    email: str,
    success: bool,
    ip: str,
    error: str | None = None,
):
    event = OAuthLoginAttemptLog(email=email, success=success, ip=ip, error=error)
    await log_publisher.publish(event)
