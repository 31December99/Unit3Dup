# -*- coding: utf-8 -*-


def handle_http_error(status_code: int):
    if status_code == 401:
        raise TMDBAuthError("Invalid or missing API key.")
    elif status_code == 404:
        raise TMDBNotFoundError("The requested resource was not found.")
    elif status_code == 429:
        raise TMDBRateLimitError("Rate limit exceeded. Too many requests.")
    else:
        raise TMDBRequestError(status_code, "HTTP error occurred.")


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
