import json

import aiohttp
import diskcache as dc
import logging
from typing import Optional
from view import custom_console
from common.external_services.Pw.sessions.exceptions import exception_handler

ENABLE_LOG = False
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)


class MyHttp:
    """Classe per gestire richieste HTTP asincrone"""

    def __init__(self, headers: dict, cache_dir: str = "http_cache"):
        self.headers = headers
        self.cache = dc.Cache(cache_dir)
        self.session: Optional[aiohttp.ClientSession] = None

    async def init_session(self):
        """Inizializza la sessione HTTP asincrona"""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers)

    def create_cache_key(self, url: str, params: dict) -> str:
        """Genera la chiave di cache in base all'URL e parametri"""
        if params:
            params = "&".join(f"{key}={val}" for key, val in sorted(params.items()))
        return f"{url}?{params}"

    @exception_handler(log_errors=ENABLE_LOG)
    async def get_url(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        data=None,
        use_cache: bool = False,
        get_method: bool = True,
    ):
        """Richiesta GET o POST asincrona"""
        #         await self.init_session()
        cache_key = self.create_cache_key(url, params or {})

        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        if get_method:
            async with self.session.get(url, params=params, headers=headers,  allow_redirects=False) as response:
                content = await response.read()
        else:
            async with self.session.post(url, params=params, headers=headers, data=data) as response:
                content = await response.read()

            # Decodifica il contenuto in bytes in formato JSON
        decoded_content = content.decode('utf-8')  # Decodifica bytes in stringa
        try:
            # Parsifica la stringa JSON in un dizionario
            json_data = json.loads(decoded_content)
        except json.JSONDecodeError as e:
            custom_console.bot_error_log(f"Errore nella decodifica del JSON: {e}")
            return None

        if use_cache:
            self.cache[cache_key] = json_data  # Salva i dati JSON nel cache

        return json_data  # Restituisci i dati parsificati come dizionario JSON


    @exception_handler(log_errors=ENABLE_LOG)
    async def post(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        data=None,
        use_cache: bool = False,
    ):
        """Richiesta POST asincrona"""
        await self.init_session()
        cache_key = self.create_cache_key(url, params or {})

        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        async with self.session.post(url, params=params, headers=headers, data=data) as response:
            content = await response.read()

        if response.status == 200:
            if use_cache:
                self.cache[cache_key] = content
            return content
        else:
            custom_console.bot_error_log(f"{self.__class__.__name__}: {content}")
            return content

    async def close(self):
        """Chiude la sessione HTTP"""
        if self.session:
            await self.session.close()
            self.cache.close()
