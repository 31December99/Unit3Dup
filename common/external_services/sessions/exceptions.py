# -*- coding: utf-8 -*-

from functools import wraps
from typing import Callable, Any
from common.custom_console import custom_console


class HttpError(Exception):
    """Base class for all exceptions raised by the HTTP client."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class HttpAuthError(HttpError):
    """Exception raised for authentication errors."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class HttpNotFoundError(HttpError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class HttpRateLimitError(HttpError):
    """Exception raised when the API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)


class HttpRequestError(HttpError):
    """Exception raised for general request errors."""

    def __init__(self, status_code: int, message: str = "Request failed"):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"HttpRequestError: {self.message} (status code: {self.status_code})"


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except HttpAuthError as e:
            custom_console.bot_error_log(f"Authentication Error: {e}")
        except HttpNotFoundError as e:
            custom_console.bot_error_log(f"Not Found Error: {e}")
        except HttpRateLimitError as e:
            custom_console.bot_error_log(f"Rate Limit Error: {e}")
        except HttpRequestError as e:
            custom_console.bot_error_log(f"Request Error: {e}")
        except Exception as e:
            custom_console.bot_error_log(f"An unexpected error occurred: '{e}'")

    return wrapper
