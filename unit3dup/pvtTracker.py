# -*- coding: utf-8 -*-
import os
import aiohttp
import asyncio
import aiofiles

import json
import hashlib
import diskcache

from view import custom_console
from common.trackers.data import trackers_api_data
from urllib.parse import urljoin



class TrackerAPIError(Exception):
    pass


class Myhttp:
    def __init__(self, tracker_name: str, pass_key=''):
        api_data = trackers_api_data.get(tracker_name.upper())
        if not api_data:
            custom_console.bot_error_log(
                f"Tracker '{tracker_name}' not found. Please check your configuration or set it using the '-t' flag.")
            raise TrackerAPIError("Invalid tracker name")

        self.base_url = api_data['url']
        self.api_token = api_data['api_key']

        self.upload_url = urljoin(self.base_url, "api/torrents/upload")
        self.filter_url = urljoin(self.base_url, "api/torrents/filter?")
        self.fetch_url = urljoin(self.base_url, "api/torrents/")
        self.tracker_announce_url = urljoin(self.base_url, f"announce/{pass_key}")

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Accept": "application/json",
        }

        # Params gets the token
        self.params = {
            "api_token": self.api_token,
        }

        self.default_data = {
            "name": "TEST.torrent",
            "description": "",
            "mediainfo": "",
            "bdinfo": " ",
            "type_id": "1",
            "resolution_id": 10,
            "tmdb": "",
            "imdb": "0",
            "tvdb": "0",
            "mal": "0",
            "igdb": "0",
            "anonymous": 0,
            "stream": "0",
            "sd": "0",
            "keywords": "",
            "personal_release": "0",
            "internal": 0,
            "featured": 0,
            "free": 0,
            "doubleup": 0,
            "sticky": 0,
        }

        self.default_params = {"api_token": self.api_token}
        self.session = aiohttp.ClientSession(headers=self.headers)


    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None


class Tracker(Myhttp):
    def __init__(self, tracker_name: str, pass_key=''):
        super().__init__(tracker_name, pass_key)
        self._cache = diskcache.Cache('./tracker_cache')
        self._cache_duration = 30

    async def _get(self, extra_params: dict) -> dict:
        params = self.default_params.copy()
        params.update(extra_params)

        key_string = json.dumps(params, sort_keys=True)
        cache_key = hashlib.sha256(key_string.encode('utf-8')).hexdigest()

        if cache_key in self._cache:
            return self._cache[cache_key]

        while True:
            try:
                async with self.session.get(self.filter_url, params=params, timeout=10) as response:
                    if response.status == 429:
                        custom_console.bot_error_log("Rate limit hit. Waiting 60 seconds...")
                        await asyncio.sleep(60)
                        continue

                    response.raise_for_status()

                    text = await response.text(encoding='utf-8', errors='ignore')

                    try:
                        data = json.loads(text)
                        self._cache.set(cache_key, data, expire=self._cache_duration)
                        return data
                    except json.JSONDecodeError as e:
                        custom_console.bot_error_log(f"Invalid response from the server {e}")
                        raise TrackerAPIError("Invalid Json") from e

            except aiohttp.ClientResponseError as e:
                custom_console.bot_error_log(f"HTTP Error {e.status}")
                raise TrackerAPIError(f"HTTP Error {e.status}") from e

            except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
                custom_console.bot_error_log("Tracker connection error or timeout.")
                raise TrackerAPIError("Tracker offline") from e

    async def _post(self, file: dict, extra_data: dict, extra_params: dict):
        data = self.default_data.copy()
        data.update(extra_data)
        params = self.default_params.copy()
        params.update(extra_params)
        form = aiohttp.FormData()

        async with aiofiles.open(file['torrent'], 'rb') as tf:
            torrent_data = await tf.read()
            filename = os.path.basename(file['torrent'])
            form.add_field('torrent',
                           torrent_data,
                           filename=filename,
                           content_type='application/octet-stream')

        if file.get('nfo'):
            async with aiofiles.open(file['nfo'], 'rb') as nf:
                nfo_data = await nf.read()
                nfo_name = os.path.basename(file['nfo'])
                form.add_field('nfo',
                               nfo_data,
                               filename=nfo_name,
                               content_type='text/plain')

        for key, value in data.items():
            if value is not None:
                form.add_field(key, str(value))

        async with self.session.post(self.upload_url, data=form, params=params, timeout=10) as response:
            return await response.json()

class Uploader(Tracker):
    async def upload_t(self, data: dict, torrent_archive_path: str, nfo_path=None) -> aiohttp.ClientResponse:
        file_torrent = {"torrent": torrent_archive_path}
        if nfo_path:
            file_torrent.update({"nfo": await self.encode_utf8(file_path=nfo_path)})

        return await self._post(file=file_torrent, extra_data=data, extra_params=self.params)

    @staticmethod
    async def encode_utf8(file_path: str) -> str:
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'latin1']
        async with aiofiles.open(file_path, 'rb') as f:
            raw_data = await f.read()

        for encoding in encodings:
            try:
                return raw_data.decode(encoding)
            except (UnicodeDecodeError, TypeError):
                continue

        return "Error: Unable to read the NFO file!"


class FilterAPI(Tracker):
    async def filter_by(self, **filters) -> dict:
        if "perPage" not in filters:
            filters["perPage"] = 100
        return await self._get(filters)


class Unit3d(FilterAPI, Uploader):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
