# -*- coding: utf-8 -*-

import io
from typing import Any

import requests
from urllib.parse import urljoin

from unit3dup.external.tracker.data import trackers_api_data
from unit3dup.external.http_client import BaseHttpClient

from unit3dup.view import custom_console


class Tracker:
    """
    Base class for API Unit3D
    """

    REQUEST_TIMEOUT = 10
    RATE_LIMIT_WAIT = 60

    def __init__(
            self,
            tracker_name: str,
            pass_key: str = "",
    ) -> None:

        api_data = self._get_tracker_config(
            tracker_name
        )

        self.pass_key = pass_key
        self.base_url = api_data["url"]
        self.api_token = api_data["api_key"]

        self.upload_url = urljoin(
            self.base_url,
            "api/torrents/upload",
        )

        self.filter_url = urljoin(
            self.base_url,
            "api/torrents/filter",
        )

        self.fetch_url = urljoin(
            self.base_url,
            "api/torrents/",
        )

        self.tracker_announce_url = urljoin(
            self.base_url,
            f"announce/{pass_key}",
        )

        self.headers = {
            "User-Agent": (
                "Unit3D-up/0.0 "
                "(Linux 5.10.0-23-amd64)"
            ),
            "Accept": "application/json",
            "Authorization": (
                f"Bearer {self.api_token}"
            ),
        }

        # HTTP Client
        self.http = BaseHttpClient(
            headers=self.headers,
            timeout=self.REQUEST_TIMEOUT,
        )

        # Parameters
        self.params: dict[str, Any] = {}

        self.data = {
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
            "mod_queue_opt_in": "0",
            "internal": 0,
            "featured": 0,
            "free": 0,
            "doubleup": 0,
            "sticky": 0,
        }

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @staticmethod
    def _get_tracker_config(
            tracker_name: str,
    ) -> dict[str, Any]:

        if not tracker_name:
            custom_console.bot_error_log(
                "No tracker specified. "
                "Please check your configuration "
                "or use the '-t' flag."
            )

            raise SystemExit(1)

        api_data = trackers_api_data.get(
            tracker_name.upper()
        )

        if not api_data:
            custom_console.bot_error_log(
                f"Tracker '{tracker_name}' not found. "
                "Please check your configuration or "
                "set it using the '-t' flag."
            )

            raise SystemExit(1)

        return api_data

    def _get(
            self,
            params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = self.http.get(
            url=self.filter_url,
            params=params,
        )

        return response.json()

    def _post(
            self,
            files: dict[str, Any],
            data: dict[str, Any],
            params: dict[str, Any] | None = None,
    ) -> requests.Response:

        return self.http.post(
            url=self.upload_url,
            files=files,
            data=data,
            params=params,
        )

    # ------------------------------------------------------------------
    # /// Torrent API
    # ------------------------------------------------------------------

    def _fetch_all(
            self,
            params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = self.http.get(
            url=self.fetch_url,
            params=params,
        )

        return response.json()

    def _fetch_id(
            self,
            torrent_id: int,
    ) -> requests.Response:

        return self.http.get(
            url=f"{self.fetch_url}{torrent_id}",
            params=self.params,
        )

    def _next_page(
            self,
            url: str,
    ) -> dict[str, Any]:

        response = self.http.get(
            url=url,
            params=self.params,
        )

        return response.json()

    # ------------------------------------------------------------------
    # Close
    # ------------------------------------------------------------------

    def close(self) -> None:
        """
        HTTP close
        """

        self.http.close()


class FilterAPI(Tracker):
    """
    Tracker filtering API
    """

    def _filter(
            self,
            key: str,
            value: Any,
            per_page: int | None = None,
    ) -> dict[str, Any]:

        params = {
            key: value,
        }

        if per_page is not None:
            params["perPage"] = per_page

        return self._get(
            params=params
        )

    # ------------------------------------------------------------------
    # ID filters
    # ------------------------------------------------------------------

    def tmdb(
            self,
            tmdb_id: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "tmdbId",
            tmdb_id,
            perPage,
        )

    def imdb(
            self,
            imdb_id: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "imdbId",
            imdb_id,
            perPage,
        )

    def igdb(
            self,
            igdb_id: int,
            perPage: int | None = None,
    ):
        custom_console.bot_warning_log(
            "The tracker has not implemented "
            "IGDB filtering yet."
        )

        raise SystemExit(1)

    def tvdb(
            self,
            tvdb_id: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "tvdbId",
            tvdb_id,
            perPage,
        )

    def mal(
            self,
            mal_id: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "malId",
            mal_id,
            perPage,
        )

    def playlist_id(
            self,
            playlistId: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "playlistId",
            playlistId,
            perPage,
        )

    def collection_id(
            self,
            collectionId: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "collectionId",
            collectionId,
            perPage,
        )

    # ------------------------------------------------------------------
    # Text filters
    # ------------------------------------------------------------------

    def name(
            self,
            name: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "name",
            name,
            perPage,
        )

    def description(
            self,
            description: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "description",
            description,
            perPage,
        )

    def mediainfo(
            self,
            mediainfo: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "mediainfo",
            mediainfo,
            perPage,
        )

    def bdinfo(
            self,
            bdinfo: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "bdinfo",
            bdinfo,
            perPage,
        )

    def file_name(
            self,
            file_name: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "file_name",
            file_name,
            perPage,
        )

    def uploader(
            self,
            uploader: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "uploader",
            uploader,
            perPage,
        )

    # ------------------------------------------------------------------
    # Year filters
    # ------------------------------------------------------------------

    def start_year(
            self,
            start_year: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "startYear",
            start_year,
            perPage,
        )

    def end_year(
            self,
            end_year: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "endYear",
            end_year,
            perPage,
        )

    # ------------------------------------------------------------------
    # Status filters
    # ------------------------------------------------------------------

    def freeleech(
            self,
            freeleech: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "free",
            freeleech,
            perPage,
        )

    def alive(
            self,
            alive: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "alive",
            alive,
            perPage,
        )

    def dying(
            self,
            dying: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "dying",
            dying,
            perPage,
        )

    def dead(
            self,
            dead: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "dead",
            dead,
            perPage,
        )

    def doubleup(
            self,
            double_up: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "doubleup",
            double_up,
            perPage,
        )

    def featured(
            self,
            featured: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "featured",
            featured,
            perPage,
        )

    def refundable(
            self,
            refundable: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "refundable",
            refundable,
            perPage,
        )

    def stream(
            self,
            stream: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "stream",
            stream,
            perPage,
        )

    def sd(
            self,
            sd: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "sd",
            sd,
            perPage,
        )

    def highspeed(
            self,
            high_speed: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "highspeed",
            high_speed,
            perPage,
        )

    def internal(
            self,
            internal: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "internal",
            internal,
            perPage,
        )

    def personal_release(
            self,
            personalRelease: bool,
            perPage: int | None = None,
    ):
        return self._filter(
            "personalRelease",
            personalRelease,
            perPage,
        )

    # ------------------------------------------------------------------
    # Numeric filters
    # ------------------------------------------------------------------

    def seasonNumber(
            self,
            seasonNumber: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "seasonNumber",
            seasonNumber,
            perPage,
        )

    def episodeNumber(
            self,
            episodeNumber: int,
            perPage: int | None = None,
    ):
        return self._filter(
            "episodeNumber",
            episodeNumber,
            perPage,
        )

    def types(
            self,
            type_id: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "types[]",
            type_id,
            perPage,
        )

    def resolution(
            self,
            res_id: str,
            perPage: int | None = None,
    ):
        return self._filter(
            "resolutions[]",
            res_id,
            perPage,
        )

    # ------------------------------------------------------------------
    # Combined filters
    # ------------------------------------------------------------------

    def tmdb_res(
            self,
            tmdb_id: int,
            res_id: str,
            perPage: int | None = None,
    ):

        params = {
            "tmdbId": tmdb_id,
            "resolutions[]": res_id,
        }

        if perPage is not None:
            params["perPage"] = perPage

        return self._get(
            params=params
        )

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------

    def next(
            self,
            url: str,
    ):
        return self._next_page(
            url=url
        )


class Torrents(Tracker):
    """
    Torrent retrieval API
    """

    def torrents(
            self,
            perPage: int | None = None,
    ):
        params = {}

        if perPage is not None:
            params["perPage"] = perPage

        return self._fetch_all(
            params=params
        )

    def torrent(
            self,
            torrent_id: int,
    ):
        return self._fetch_id(
            torrent_id=torrent_id
        )


class Uploader(Tracker):
    """
    Torrent upload API
    """

    def upload_t(
            self,
            data: dict,
            torrent_archive_path: str,
            nfo_path: str | None = None,
    ) -> requests.Response:

        files = {}

        with open(
                torrent_archive_path,
                "rb",
        ) as torrent_file:
            files["torrent"] = (
                "upload.torrent",
                torrent_file,
                "application/x-bittorrent",
            )

            if nfo_path:
                with open(
                        nfo_path,
                        "rb",
                ) as nfo_file:
                    files["nfo"] = (
                        "file.nfo",
                        nfo_file,
                        "text/plain",
                    )

                    return self._post(
                        files=files,
                        data=data,
                        params=self.params,
                    )

            return self._post(
                files=files,
                data=data,
                params=self.params,
            )

    @staticmethod
    def encode_utf8(
            file_path: str,
    ) -> bytes | io.BytesIO:

        encodings = (
            "utf-8",
            "iso-8859-1",
            "windows-1252",
            "latin1",
        )

        with open(
                file_path,
                "rb",
        ) as file:

            raw_data = file.read()

        for encoding in encodings:

            try:

                decoded_content = raw_data.decode(
                    encoding
                )

                return decoded_content.encode(
                    "utf-8"
                )

            except UnicodeDecodeError:

                continue

        error_message = (
            "Error: Unable to read the NFO file!"
        )

        return io.BytesIO(
            error_message.encode("utf-8")
        )


class Unit3d(
    FilterAPI,
    Torrents,
    Uploader,
):
    """
    Main Unit3D API facade

    Combines:
    - Tracker filtering
    - Torrent retrieval
    - Torrent upload
    """

    # ------------------------------------------------------------------
    # ID filters
    # ------------------------------------------------------------------

    def get_tmdb(
            self,
            tmdb_id: int,
            perPage: int | None = None,
    ):
        return self.tmdb(
            tmdb_id=tmdb_id,
            perPage=perPage,
        )

    def get_tvdb(
            self,
            tvdb_id: int,
            perPage: int | None = None,
    ):
        return self.tvdb(
            tvdb_id=tvdb_id,
            perPage=perPage,
        )

    def get_imdb(
            self,
            imdb_id: int,
            perPage: int | None = None,
    ):
        return self.imdb(
            imdb_id=imdb_id,
            perPage=perPage,
        )

    def get_igdb(
            self,
            igdb_id: int,
            perPage: int | None = None,
    ):
        return self.igdb(
            igdb_id=igdb_id,
            perPage=perPage,
        )

    def get_mal(
            self,
            mal_id: int,
            perPage: int | None = None,
    ):
        return self.mal(
            mal_id=mal_id,
            perPage=perPage,
        )

    def get_playlist_id(
            self,
            playlist_id: int,
            perPage: int | None = None,
    ):
        return self.playlist_id(
            playlistId=playlist_id,
            perPage=perPage,
        )

    def get_collection_id(
            self,
            collection_id: int,
            perPage: int | None = None,
    ):
        return self.collection_id(
            collectionId=collection_id,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Text filters
    # ------------------------------------------------------------------

    def get_name(
            self,
            name: str,
            perPage: int | None = None,
    ):
        return self.name(
            name=name,
            perPage=perPage,
        )

    def get_description(
            self,
            description: str,
            perPage: int | None = None,
    ):
        return self.description(
            description=description,
            perPage=perPage,
        )

    def get_bdinfo(
            self,
            bdinfo: str,
            perPage: int | None = None,
    ):
        return self.bdinfo(
            bdinfo=bdinfo,
            perPage=perPage,
        )

    def get_mediainfo(
            self,
            mediainfo: str,
            perPage: int | None = None,
    ):
        return self.mediainfo(
            mediainfo=mediainfo,
            perPage=perPage,
        )

    def get_uploader(
            self,
            uploader: str,
            perPage: int | None = None,
    ):
        return self.uploader(
            uploader=uploader,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Year filters
    # ------------------------------------------------------------------

    def after_start_year(
            self,
            start_year: str,
            perPage: int | None = None,
    ):
        return self.start_year(
            start_year=start_year,
            perPage=perPage,
        )

    def before_end_year(
            self,
            end_year: str,
            perPage: int | None = None,
    ):
        return self.end_year(
            end_year=end_year,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Status filters
    # ------------------------------------------------------------------

    def get_freeleech(
            self,
            freeleech: int,
            perPage: int | None = None,
    ):
        return self.freeleech(
            freeleech=freeleech,
            perPage=perPage,
        )

    def get_alive(
            self,
            alive: bool,
            perPage: int | None = None,
    ):
        return self.alive(
            alive=alive,
            perPage=perPage,
        )

    def get_dying(
            self,
            dying: bool,
            perPage: int | None = None,
    ):
        return self.dying(
            dying=dying,
            perPage=perPage,
        )

    def get_dead(
            self,
            dead: bool,
            perPage: int | None = None,
    ):
        return self.dead(
            dead=dead,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Media filters
    # ------------------------------------------------------------------

    def get_filename(
            self,
            file_name: str,
            perPage: int | None = None,
    ):
        return self.file_name(
            file_name=file_name,
            perPage=perPage,
        )

    def get_season_number(
            self,
            se_number: int,
            perPage: int | None = None,
    ):
        return self.seasonNumber(
            seasonNumber=se_number,
            perPage=perPage,
        )

    def get_episode_number(
            self,
            ep_number: int,
            perPage: int | None = None,
    ):
        return self.episodeNumber(
            episodeNumber=ep_number,
            perPage=perPage,
        )

    def get_types(
            self,
            type_id: str,
            perPage: int | None = None,
    ):
        if not type_id:
            return None

        return self.types(
            type_id=type_id,
            perPage=perPage,
        )

    def get_res(
            self,
            res_id: str,
            perPage: int | None = None,
    ):
        if not res_id:
            return None

        return self.resolution(
            res_id=res_id,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Torrent retrieval
    # ------------------------------------------------------------------

    def fetch_all(
            self,
            perPage: int | None = None,
    ):
        return self.torrents(
            perPage=perPage
        )

    def fetch_id(
            self,
            torrent_id: int,
    ):
        return self.torrent(
            torrent_id=torrent_id
        )

    # ------------------------------------------------------------------
    # /// Boolean filters
    # ------------------------------------------------------------------

    def get_double_up(
            self,
            double_up: bool,
            perPage: int | None = None,
    ):
        return self.doubleup(
            double_up=double_up,
            perPage=perPage,
        )

    def get_featured(
            self,
            featured: bool,
            perPage: int | None = None,
    ):
        return self.featured(
            featured=featured,
            perPage=perPage,
        )

    def get_refundable(
            self,
            refundable: bool,
            perPage: int | None = None,
    ):
        return self.refundable(
            refundable=refundable,
            perPage=perPage,
        )

    def get_stream(
            self,
            stream: bool,
            perPage: int | None = None,
    ):
        return self.stream(
            stream=stream,
            perPage=perPage,
        )

    def get_sd(
            self,
            sd: bool,
            perPage: int | None = None,
    ):
        return self.sd(
            sd=sd,
            perPage=perPage,
        )

    def get_highspeed(
            self,
            highspeed: bool,
            perPage: int | None = None,
    ):
        return self.highspeed(
            high_speed=highspeed,
            perPage=perPage,
        )

    def get_internal(
            self,
            internal: bool,
            perPage: int | None = None,
    ):
        return self.internal(
            internal=internal,
            perPage=perPage,
        )

    def get_personal_release(
            self,
            personalRelease: bool,
            perPage: int | None = None,
    ):
        return self.personal_release(
            personalRelease=personalRelease,
            perPage=perPage,
        )

    # ------------------------------------------------------------------
    # /// Combined filters
    # ------------------------------------------------------------------

    def get_tmdb_res(
            self,
            tmdb_id: int,
            res_id: str,
            perPage: int | None = None,
    ):
        if not tmdb_id or not res_id:
            return None

        return self.tmdb_res(
            tmdb_id=tmdb_id,
            res_id=res_id,
            perPage=perPage,
        )
