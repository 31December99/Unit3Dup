# -*- coding: utf-8 -*-

from functools import wraps
from typing import Callable, Any
from common.custom_console import custom_console


class TMDBError(Exception):
    """Base class for all exceptions raised by the TMDB API package."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TMDBAuthError(TMDBError):
    """Exception raised for authentication errors with the TMDB API."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class TMDBNotFoundError(TMDBError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class TMDBRateLimitError(TMDBError):
    """Exception raised when the TMDB API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)


class TMDBRequestError(TMDBError):
    """Exception raised for general request errors."""

    def __init__(self, status_code: int, message: str = "Request failed"):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"TMDBRequestError: {self.message} (status code: {self.status_code})"


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TMDBAuthError as e:
            custom_console.bot_error_log(f"Authentication Error: {e}")
        except TMDBNotFoundError as e:
            custom_console.bot_error_log(f"Not Found Error: {e}")
        except TMDBRateLimitError as e:
            custom_console.bot_error_log(f"Rate Limit Error: {e}")
        except TMDBRequestError as e:
            custom_console.bot_error_log(f"Request Error: {e}")
        except Exception as e:
            custom_console.bot_error_log(f"An unexpected error occurred: '{e}'")

    return wrapper
