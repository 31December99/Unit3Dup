# -*- coding: utf-8 -*-

import httpx
from functools import wraps
from typing import Callable, Any
from view import custom_console


class HttpError(Exception):
    """Base class for all exceptions raised by the HTTP client."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# passare httpx anche agli altri
class ConnectError(httpx.ConnectError, HttpError):
    """Custom exception raised for connection errors."""
    def __init__(self, message: str = "Connection error"):
        super().__init__(message)


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

    def __init__(self, message: str = "Request failed"):
        super().__init__(message)


def exception_handler(log_errors: bool = True) -> Callable[..., Any]:
    """
    Decorator for handling exceptions and optionally logging them.

    Args:
        log_errors (bool): Whether to log the errors. If True, errors will be logged.

    Returns:
        Callable[..., Any]: The decorator that handles exceptions.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                response = func(*args, **kwargs)
                if response.status_code == 404:
                    raise HttpNotFoundError()
                elif response.status_code == 401:
                    raise HttpAuthError()
                elif response.status_code == 429:
                    raise HttpRateLimitError()
                elif response.status_code >= 400:
                    raise HttpRequestError()
                return response

            except httpx.ConnectError as e:
                if log_errors:
                    custom_console.bot_error_log(f"Connection Error: {e}")

            except HttpAuthError as e:
                if log_errors:
                    custom_console.bot_error_log(f"Authentication Error: {e}")

            except HttpNotFoundError as e:
                if log_errors:
                    custom_console.bot_error_log(f"Not Found Error: {e}")

            except HttpRateLimitError as e:
                if log_errors:
                    custom_console.bot_error_log(f"Rate Limit Error: {e}")

            except HttpRequestError as e:
                if log_errors:
                    custom_console.bot_error_log(f"Request Error: {e}")

        return wrapper

    return decorator
