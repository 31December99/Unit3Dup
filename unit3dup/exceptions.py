# -*- coding: utf-8 -*-
from functools import wraps
from typing import Callable, Any
from view import custom_console


class Unit3DError(Exception):
    """Base class for all exceptions raised by the Unit3D API package"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class Unit3DBadRequestError(Unit3DError):
    """Exception raised for bad requests to the Unit3D API."""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message)


class Unit3DAuthError(Unit3DError):
    """Exception raised for authentication errors with the Unit3D API."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class Unit3DForbiddenError(Unit3DError):
    """Exception raised for forbidden access to resources."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message)


class Unit3DNotFoundError(Unit3DError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class Unit3DConflictError(Unit3DError):
    """Exception raised for conflicts in the request."""

    def __init__(self, message: str = "Request conflict"):
        super().__init__(message)


class Unit3DRateLimitError(Unit3DError):
    """Exception raised when the Unit3D API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)


class Unit3DServerError(Unit3DError):
    """Exception raised for internal server errors."""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(message)


class Unit3DServiceUnavailableError(Unit3DError):
    """Exception raised when the service is unavailable."""

    def __init__(self, message: str = "Service unavailable"):
        super().__init__(message)


class Unit3DRequestError(Unit3DError):
    """Exception raised for general request errors."""

    def __init__(self, status_code: int, message: str = "Request failed"):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"Unit3DRequestError: {self.message} (status code: {self.status_code})"


class BotConfigError(Unit3DError):
    """Exception raised for general request errors."""

    def __init__(self, message: str = "Loading failed"):
        super().__init__(message)

    def __str__(self):
        return f"BotConfigError: {self.message}"


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Unit3DBadRequestError as e:
            custom_console.bot_error_log(f"Bad Request Error: {e}")
        except Unit3DAuthError as e:
            custom_console.bot_error_log(f"Authentication Error: {e}")
        except Unit3DForbiddenError as e:
            custom_console.bot_error_log(f"Forbidden Error: {e}")
        except Unit3DNotFoundError as e:
            custom_console.bot_error_log(f"Not Found Error: {e}")
        except Unit3DConflictError as e:
            custom_console.bot_error_log(f"Conflict Error: {e}")
        except Unit3DRateLimitError as e:
            custom_console.bot_error_log(f"Rate Limit Error: {e}")
        except Unit3DServerError as e:
            custom_console.bot_error_log(f"Server Error: {e}")
        except Unit3DServiceUnavailableError as e:
            custom_console.bot_error_log(f"Service Unavailable Error: {e}")
        except Unit3DRequestError as e:
            custom_console.bot_error_log(f"Request Error: {e}")
        except BotConfigError as e:
            custom_console.bot_error_log(f" {e}")
            exit(1)

        except Exception as e:
            custom_console.bot_error_log(f"An unexpected error occurred: '{e}'")

    return wrapper
