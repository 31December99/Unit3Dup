# -*- coding: utf-8 -*-

import hashlib
import time
from typing import Any

import diskcache
import requests

from unit3dup.view import custom_console


class BaseHttpClient:
    """
    HTTP client for TMDB and tracker code
    """

    REQUEST_TIMEOUT = 10
    RATE_LIMIT_WAIT = 60

    def __init__(
            self,
            headers: dict[str, str] | None = None,
            timeout: int = REQUEST_TIMEOUT,
            cache_dir: str = "http_cache",
    ) -> None:

        self.session = requests.Session()
        self.timeout = timeout

        if headers:
            self.session.headers.update(
                headers
            )

        self.cache = diskcache.Cache(
            cache_dir
        )

    # ==================================================================
    # /// CACHE
    # ==================================================================

    @staticmethod
    def create_cache_key(
            url: str,
            params: dict[str, Any] | None = None,
    ) -> str:
        """
        Create a unique cache key from URL and parameters
        """

        if params:

            sorted_params = "&".join(
                f"{key}={value}"
                for key, value in sorted(
                    params.items()
                )
            )

        else:

            sorted_params = ""

        raw_key = (
            f"{url}?{sorted_params}"
        )

        return hashlib.md5(
            raw_key.encode(
                "utf-8"
            )
        ).hexdigest()

    def _get_cached_response(
            self,
            cache_key: str,
    ) -> requests.Response | None:
        """
        Restore a Response object from cache
        """

        if cache_key not in self.cache:
            return None

        response_data = self.cache[
            cache_key
        ]

        response = requests.Response()

        response.status_code = (
            response_data[
                "status_code"
            ]
        )

        response.headers.update(
            response_data[
                "headers"
            ]
        )

        response._content = (
            response_data[
                "content"
            ]
        )

        response.url = (
            response_data.get(
                "url"
            )
        )

        return response

    def _cache_response(
            self,
            cache_key: str,
            response: requests.Response,
    ) -> None:
        """
        Store a Response object in the HTTP cache
        """

        self.cache[
            cache_key
        ] = {
            "status_code": (
                response.status_code
            ),
            "headers": dict(
                response.headers
            ),
            "content": response.content,
            "url": response.url,
        }

    # ==================================================================
    # INTERNAL HTTP REQUEST
    # ==================================================================

    def _request(
            self,
            method: str,
            url: str,
            params: dict[str, Any] | None = None,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | None = None,
            files: dict[str, Any] | None = None,
            use_cache: bool = False,
    ) -> requests.Response:
        """
        Handle HTTP requests through a single internal method
        """

        method = method.upper()

        cache_key = self.create_cache_key(
            url=url,
            params=params,
        )

        # Check cache

        if use_cache:

            cached_response = (
                self._get_cached_response(
                    cache_key
                )
            )

            if cached_response:
                return cached_response

        # Send request
        while True:

            try:

                response = self.session.request(
                    method=method,
                    url=url,
                    params=params or {},
                    headers=headers,
                    data=data,
                    files=files,
                    timeout=self.timeout,
                )

                # Handle rate limit

                if (
                        response.status_code
                        == 429
                ):
                    custom_console.bot_error_log(
                        "HTTP 429: Rate limit "
                        "reached. "
                        f"Waiting "
                        f"{self.RATE_LIMIT_WAIT} "
                        "seconds..."
                    )

                    time.sleep(
                        self.RATE_LIMIT_WAIT
                    )

                    continue

                response.raise_for_status()

                # Store response in cache

                if use_cache:
                    self._cache_response(
                        cache_key=cache_key,
                        response=response,
                    )

                return response

            except requests.exceptions.HTTPError as exc:

                status_code = (
                    exc.response.status_code
                    if exc.response is not None
                    else None
                )

                custom_console.bot_error_log(
                    f"HTTP Error "
                    f"{status_code}: "
                    f"{exc}"
                )

                raise

            except requests.exceptions.ConnectionError:

                custom_console.bot_error_log(
                    "Connection error. "
                    "Please check your network "
                    "connection or verify if the "
                    "server is online."
                )

                raise

            except requests.exceptions.Timeout as exc:

                custom_console.bot_error_log(
                    f"HTTP Timeout: {exc}"
                )

                raise

            except requests.exceptions.RequestException as exc:

                custom_console.bot_error_log(
                    f"HTTP Request Error: "
                    f"{exc}"
                )

                raise

    # ==================================================================
    # SESSION
    # ==================================================================

    def get_session(
            self,
    ) -> requests.Session:
        """
        Return the shared requests.Session
        """

        return self.session

    # ==================================================================
    # /// GET
    # ==================================================================

    def get(
            self,
            url: str,
            params: dict[str, Any] | None = None,
            use_cache: bool = False,
    ) -> requests.Response:
        """
        Execute an HTTP GET request

        Used mainly by the tracker
        """

        return self._request(
            method="GET",
            url=url,
            params=params,
            use_cache=use_cache,
        )

    # ==================================================================
    # /// GET URL
    # ==================================================================

    def get_url(
            self,
            url: str,
            params: dict[str, Any] | None = None,
            headers: dict[str, str] | None = None,
            use_cache: bool = False,
    ) -> requests.Response:
        """
        Execute an HTTP GET request

        Kept for TMDB compatibility
        """

        return self._request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
            use_cache=use_cache,
        )

    # ==================================================================
    # /// POST
    # ==================================================================

    def post(
            self,
            url: str,
            data: dict[str, Any] | None = None,
            files: dict[str, Any] | None = None,
            params: dict[str, Any] | None = None,
            headers: dict[str, str] | None = None,
            use_cache: bool = False,
    ) -> requests.Response:
        """
        Execute an HTTP POST request

        Used mainly by the tracker
        """

        return self._request(
            method="POST",
            url=url,
            params=params,
            headers=headers,
            data=data,
            files=files,
            use_cache=use_cache,
        )

    # ==================================================================
    # /// CACHE
    # ==================================================================

    def clear_cache(
            self,
    ) -> None:
        """
        Clear the HTTP cache
        """

        self.cache.clear()

    def close(
            self,
    ) -> None:
        """
        Close the HTTP session and cache
        """

        self.session.close()
        self.cache.close()

    # ==================================================================
    # /// CONTEXT
    # ==================================================================

    def __enter__(
            self,
    ) -> "BaseHttpClient":

        return self

    def __exit__(
            self,
            exc_type,
            exc_value,
            traceback,
    ) -> None:

        self.close()
