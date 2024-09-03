# -*- coding: utf-8 -*-

import httpx
import diskcache as dc


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

    def get_url(self, url: str, params: dict, use_cache: bool = True) -> httpx.Response:
        """
        GET request to the specified URL

        Args:
            url (str): The URL to request
            use_cache (bool): Whether to use cached response if available
            params:

        Returns:
            httpx.Response: The response object from the GET request
        """
        if use_cache and url in self.cache:
            response_data = self.cache[url]
            response = httpx.Response(
                status_code=response_data["status_code"],
                headers=response_data["headers"],
                content=response_data["content"],
            )
            return response

        response = self.session.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        if use_cache:
            # Store response in cache
            self.cache[url] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content,
            }

        return response

    def clear_cache(self):
        """Clears the HTTP response cache"""
        self.cache.clear()

    def close(self):
        """Closes the HTTP client session"""
        if self.session:
            self.session.close()
        self.cache.close()
