from abc import ABC, abstractmethod
from datetime import UTC, datetime


class LogEvent(ABC):
    @abstractmethod
    def to_dict(self) -> dict: ...


class UserEventLog(LogEvent):
    def __init__(
        self,
        email: str,
        success: bool,
        ip: str,
        error: str | None = None,
        event: str = "generic_event",
    ):
        self.event = event
        self.email = email
        self.success = success
        self.ip = ip
        self.error = error

    def to_dict(self) -> dict:
        return {
            "event": self.event,
            "email": self.email,
            "success": self.success,
            "ip": self.ip,
            "error": self.error,
            "timestamp": datetime.now(UTC).isoformat(),
        }


class UserLoginAttemptLog(UserEventLog):
    def __init__(self, email: str, success: bool, ip: str, error: str | None = None):
        super().__init__(email, success, ip, error, event="user_login_attempt")


class UserRegistrationAttemptLog(UserEventLog):
    def __init__(self, email: str, success: bool, ip: str, error: str | None = None):
        super().__init__(email, success, ip, error, event="user_registration_attempt")


class OAuthLoginAttemptLog(UserEventLog):
    def __init__(self, email: str, success: bool, ip: str, error: str | None = None):
        super().__init__(email, success, ip, error, event="user_oath_auth_attempt")


class SprintEventLog(LogEvent):
    def __init__(
        self,
        user_id: int,
        email: str,
        success: bool,
        duration: int,
        ip: str,
        error: str | None = None,
        event: str = "generic_event",
    ):
        self.event = event
        self.user_id = user_id
        self.email = email
        self.success = success
        self.duration = duration
        self.ip = ip
        self.error = error

    def to_dict(self) -> dict:
        return {
            "event": self.event,
            "user_id": self.user_id,
            "email": self.email,
            "success": self.success,
            "ip": self.ip,
            "error": self.error,
            "duration": self.duration,
            "timestamp": datetime.now(UTC).isoformat(),
        }


class SaveSprintAttemptLog(SprintEventLog):
    def __init__(
        self,
        user_id: int,
        email: str,
        success: bool,
        duration: int,
        ip: str,
        error: str | None = None,
    ):
        super().__init__(
            user_id, email, success, duration, ip, error, event="save_sprint_attempt"
        )


class CategoryEventLog(LogEvent):
    def __init__(
        self,
        *,
        event: str,
        user_id: int,
        email: str,
        success: bool,
        category_id: int | None = None,
        category_name: str | None = None,
        ip: str = "",
        error: str | None = None,
        **extra,
    ):
        self.event = event
        self.user_id = user_id
        self.email = email
        self.success = success
        self.category_id = category_id
        self.category_name = category_name
        self.ip = ip
        self.error = error
        self.extra = extra

    def to_dict(self) -> dict:
        base = {
            "event": self.event,
            "user_id": self.user_id,
            "email": self.email,
            "success": self.success,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "ip": self.ip,
            "error": self.error,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        return {**base, **self.extra}


class CreateCategoryAttemptLog(CategoryEventLog):
    def __init__(self, **kwargs):
        super().__init__(event="create_category_attempt", **kwargs)


class GetCategoriesAttemptLog(CategoryEventLog):
    def __init__(self, categories_count: int | None = None, **kwargs):
        super().__init__(
            event="get_categories_attempt", categories_count=categories_count, **kwargs
        )


class DeleteCategoryAttemptLog(CategoryEventLog):
    def __init__(self, **kwargs):
        super().__init__(event="delete_category_attempt", **kwargs)


class UpdateCategoryAttemptLog(CategoryEventLog):
    def __init__(self, **kwargs):
        super().__init__(event="update_category_attempt", **kwargs)


class JournalEventLog(LogEvent):
    def __init__(
        self,
        *,
        event: str,
        user_id: int,
        email: str,
        success: bool,
        entry_id: int | None = None,
        ip: str = "",
        error: str | None = None,
        **extra,
    ):
        self.event = event
        self.user_id = user_id
        self.email = email
        self.success = success
        self.entry_id = entry_id
        self.ip = ip
        self.error = error
        self.extra = extra

    def to_dict(self) -> dict:
        base = {
            "event": self.event,
            "user_id": self.user_id,
            "email": self.email,
            "success": self.success,
            "entry_id": self.entry_id,
            "ip": self.ip,
            "error": self.error,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        return {**base, **self.extra}
