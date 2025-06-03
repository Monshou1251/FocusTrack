from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict

class LogEvent(ABC):
    @abstractmethod
    def to_dict(self) -> Dict: ...

class UserEventLog(LogEvent):
    def __init__(self, email: str, success: bool, ip: str, error: str | None = None, event: str = "generic_event"):
        self.event = event
        self.email = email
        self.success = success
        self.ip = ip
        self.error = error

    def to_dict(self) -> Dict:
        return {
            "event": self.event,
            "email": self.email,
            "success": self.success,
            "ip": self.ip,
            "error": self.error,
            "timestamp": datetime.now(timezone.utc).isoformat()
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
        