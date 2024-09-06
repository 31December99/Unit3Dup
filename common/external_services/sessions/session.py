# -*- coding: utf-8 -*-

import httpx
import diskcache as dc
from common.external_services.sessions.exceptions import exception_handler

ENABLE_LOG = True


class MyHttp:
    """Class to handle HTTP requests"""

    def __init__(self, headers: dict, cache_dir: str = "http_cache"):
        self.session = httpx.Client(
            timeout=httpx.Timeout(30), headers=headers, verify=False
        )
        self.headers = headers
        self.cache = dc.Cache(cache_dir)

    def get_session(self) -> httpx.Client:
        """Returns the HTTP session"""
        return self.session

    @staticmethod
    def create_cache_key(url: str, params: dict) -> str:
        """ Generates the cache key based on the URL and query parameters (otherwise the resource is not updated in
        the cache.. """

        # Add the query to the cached endpoint
        # Sorted params to avoid duplicate
        params = "&".join(f"{key}={val}" for key, val in sorted(params.items()))
        return f"{url}?{params}"

    @exception_handler(log_errors=ENABLE_LOG)
    def get_url(self, url: str, params: dict, use_cache: bool = True) -> (httpx.Response, str):
        """
        GET request to the specified URL

        Args:
            url (str): The URL to request
            use_cache (bool): Whether to use cached response if available
            params (dict): The query parameters for the request

        Returns:
            httpx.Response: The response object from the GET request
        """
        cache_key = self.create_cache_key(url, params)

        if use_cache and cache_key in self.cache:
            response_data = self.cache[cache_key]
            response = httpx.Response(
                status_code=response_data["status_code"],
                headers=response_data["headers"],
                content=response_data["content"],
            )
            return response, url

        response = self.session.get(url, params=params)

        if use_cache:
            self.cache[cache_key] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content,
            }

        return response, url

    def clear_cache(self):
        """Clears the HTTP response cache"""
        self.cache.clear()

    def close(self):
        """Closes the HTTP client session"""
        if self.session:
            self.session.close()
        self.cache.close()
