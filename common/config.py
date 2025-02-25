# -*- coding: utf-8 -*-

import os
import sys
import ipaddress
from functools import cache
from pathlib import Path
from urllib.parse import urlparse

from common.custom_console import custom_console
from common.utility import ManageTitles

from pydantic_settings import BaseSettings
from pydantic import model_validator
from dotenv import load_dotenv



service_filename = "Unit3Dbot_service.env"

def create_default_env_file(path: Path):
    """
    Creates a default configuration file if it doesn't already exist
    """
    default_content = """
################################################## CONFIG ###################################################
# TRACKER CONFIG KEY
ITT_URL=https://itatorrents.xyz
ITT_APIKEY=

# TMDB CONFIG KEY
TMDB_APIKEY=

# IMAGE UPLOADERS CONFIG KEY
IMGBB_KEY=no_key
FREE_IMAGE_KEY=no_key
LENSDUMP_KEY=no_key
PTSCREENS_KEY=no_key
IMGFI_KEY=no_key

# TRAILERS KEY
YOUTUBE_KEY=no_apikey

# IGDB CONFIG
IGDB_CLIENT_ID=client_id
IGDB_ID_SECRET=secret

# QBITTORRENT CONFIG CLIENT LOGIN
QBIT_USER=
QBIT_PASS=
QBIT_HOST=http://localhost
QBIT_PORT=8080

# TRANSMISSION CONFIG CLIENT LOGIN
TRASM_USER=
TRASM_PASS=
TRASM_HOST=http://localhost
TRASM_PORT=9091

# SET DEFAULT TORRENT CLIENT
# Qbittorrent: TORRENT_CLIENT=qbittorrent
# Transmission: TORRENT_CLIENT=transmission
TORRENT_CLIENT=

############################################## USER PREFERENCES ##############################################
# Image uploader priority. 0=first in list
PTSCREENS_PRIORITY=0
LENSDUMP_PRIORITY=1
FREE_IMAGE_PRIORITY=2
IMGBB_PRIORITY=3
IMGFI_PRIORITY=4

# ------------------------------------------------------------------------------------------------------------

# Youtube favorite channel Trailers i.e : FilmsNow it
YOUTUBE_FAV_CHANNEL_ID=UCGCbxpnt25hWPFLSbvwfg_w

# Enable to use the YouTube favorite Channel otherwise perform a global search
YOUTUBE_CHANNEL_ENABLE=False

# ------------------------------------------------------------------------------------------------------------

# Search for possible candidates for duplicate files
DUPLICATE_ON=False

# auto Skip duplicates if founds
SKIP_DUPLICATE=False

# Discard videos whose size deviates by more than the specified percentage (size_th) from the video in tracker
# delta(%) < SIZE_TH = duplicate
SIZE_TH=50

# ------------------------------------------------------------------------------------------------------------

# Watch the folder watcher_path at regular intervals (watcher_interval seconds) 
WATCHER_INTERVAL=60
# It will move media from the 'watcher_path' to the 'watcher_destination_path' and upload it'
WATCHER_PATH=watcher_path
WATCHER_DESTINATION_PATH=.

# ------------------------------------------------------------------------------------------------------------

# Number of screenshots we create
NUMBER_OF_SCREENSHOTS=4

# Level of compression for screenshot 0-9 (quality) 0 = Best quality
COMPRESS_SCSHOT=4

# Resize image before sending to image hosting 
RESIZE_SCSHOT=False

# ------------------------------------------------------------------------------------------------------------

# Path for each torrent file created
TORRENT_ARCHIVE=.

# Torrent file comment (max 100 chars)
TORRENT_COMMENT=no_comment

# ------------------------------------------------------------------------------------------------------------

# Preferred language. Discard videos with a language different from preferred_lang (default=all)
# [ "ENG", "USA","ITA", "DEU", "FRA",  "GBR", "ESP", "JPN", "BRA", "RUS", "CHN"]
PREFERRED_LANG=all

# ------------------------------------------------------------------------------------------------------------

# Hide your nickname (only the nick name)
ANON=False

# ------------------------------------------------------------------------------------------------------------

# Active the cache for the screenshots
CACHE_SCR=False

# ------------------------------------------------------------------------------------------------------------
############################################## OPTIONS #######################################################
# PW - not implemented yet -
PW_API_KEY=no_key
PW_URL=http://localhost:9696/api/v1

# PW Torrent archive
PW_TORRENT_ARCHIVE_PATH=.

# PW download folder
PW_DOWNLOAD=.

# FTPX (FTPD)
FTPX_USER=user
FTPX_PASS=pass
FTPX_IP=127.0.0.1
FTPX_PORT=2121
FTPX_LOCAL_PATH=.
FTPX_ROOT=.
FTPX_KEEP_ALIVE=False
    """
    with open(path, "w") as f:
        f.write(default_content.strip())



class Config(BaseSettings):
    """
    Class to manage the configuration and validation of environment variables
    """

    ITT_URL: str = "https://itatorrents.xyz"
    ITT_APIKEY: str | None = None

    # // DB Online
    TMDB_APIKEY: str | None = None

    # // Image Host
    LENSDUMP_KEY: str | None = None
    FREE_IMAGE_KEY: str | None = None
    PTSCREENS_KEY: str | None = None
    IMGBB_KEY: str | None = None
    IMGFI_KEY: str | None = None

    # // Image Host priority
    FREE_IMAGE_PRIORITY: int = 0
    PTSCREENS_PRIORITY: int =  1
    IMGBB_PRIORITY: int = 2
    LENSDUMP_PRIORITY: int = 3
    IMGFI_PRIORITY: int = 4

    # // Trailers
    YOUTUBE_KEY: str | None = None

    # // Qbittorrent
    QBIT_USER: str | None = None
    QBIT_PASS: str | None = None
    QBIT_HOST: str = "127.0.0.1"
    QBIT_PORT: str = "8080"

    # // Transmission
    TRASM_USER: str | None = None
    TRASM_PASS: str | None = None
    TRASM_HOST: str = "127.0.0.1"
    TRASM_PORT: str = "9091"

    TORRENT_CLIENT: str | None = None

    PW_API_KEY: str | None = None
    PW_URL: str = "http://localhost:9696/api/v1"
    PW_TORRENT_ARCHIVE_PATH: str | None = None
    PW_DOWNLOAD_PATH: str | None = None

    FTPX_USER: str | None = None
    FTPX_PASS: str | None = None
    FTPX_IP: str | None = None
    FTPX_PORT: str = "2121"

    IGDB_CLIENT_ID: str | None = None
    IGDB_ID_SECRET: str | None = None


    YOUTUBE_FAV_CHANNEL_ID: str | None = None
    YOUTUBE_CHANNEL_ENABLE: bool = False

    DUPLICATE_ON: bool = False
    SKIP_DUPLICATE: bool = False
    NUMBER_OF_SCREENSHOTS: int = 6
    COMPRESS_SCSHOT: int = 4
    RESIZE_SCSHOT: bool = False
    ANON: bool = False
    CACHE_SCR: bool = False

    WATCHER_PATH: str | None = None
    WATCHER_DESTINATION_PATH: str | None = None
    WATCHER_INTERVAL: int = 60

    TORRENT_ARCHIVE: str | None = None
    TORRENT_COMMENT: str | None = None
    PREFERRED_LANG: str | None = None
    SIZE_TH: int = 100

    FTPX_LOCAL_PATH: str | None = None
    FTPX_ROOT: str = "."
    FTPX_KEEP_ALIVE: bool = False

    if os.name == "nt":
        default_env_path: Path = Path(os.getenv("LOCALAPPDATA", ".")) / f"{service_filename}"
        torrent_archive_path: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "torrent_archive"
        default_env_path_cache: Path = Path(os.getenv("LOCALAPPDATA", ".")) / f"Unit3Dup_cache"
        PW_TORRENT_ARCHIVE_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "pw_torrent_archive"
        PW_DOWNLOAD_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "pw_download"
        WATCHER_DESTINATION_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "watcher_destination_path"

    else:
        default_env_path: Path = Path.home() / f"{service_filename}"
        torrent_archive_path: Path = Path.home() / "torrent_archive"
        default_env_path_cache: Path = Path.home() / "Unit3Dup_cache"
        PW_TORRENT_ARCHIVE_PATH: Path = Path.home() / "pw_torrent_archive"
        PW_DOWNLOAD_PATH: Path = Path.home() /  "pw_download"
        WATCHER_DESTINATION_PATH: Path = Path.home()  / "watcher_destination_path"

    if not PW_TORRENT_ARCHIVE_PATH.exists():
        print(f"Create default pw torrent archive path: {PW_TORRENT_ARCHIVE_PATH}")
        os.makedirs(PW_TORRENT_ARCHIVE_PATH)

    if not PW_DOWNLOAD_PATH.exists():
        print(f"Create default pw download path: {PW_DOWNLOAD_PATH}")
        os.makedirs(PW_DOWNLOAD_PATH)

    if not WATCHER_DESTINATION_PATH.exists():
        print(f"Create default destination watcher path: {WATCHER_DESTINATION_PATH}")
        os.makedirs(WATCHER_DESTINATION_PATH)

    if not default_env_path.exists():
        print(f"Create default configuration file: {default_env_path}")
        create_default_env_file(default_env_path)

    if not torrent_archive_path.exists():
        # print(f"Create default torrent archive path: {torrent_archive_path}")
        os.makedirs(torrent_archive_path, exist_ok=True)

    if not default_env_path_cache.exists():
        # print(f"Create default cache path: {default_env_path_cache}")
        os.makedirs(default_env_path_cache, exist_ok=True)

    load_dotenv(dotenv_path=default_env_path)

    @staticmethod
    def wait_for_user_confirmation():
        # Wait for user confirmation in case of validation failure
        custom_console.bot_log(f"Please update your config file *.env")
        sys.exit(0)

    @model_validator(mode='before')
    def validate_fields(cls, values: dict) -> dict:
        """
        Validates
        """
        def validate_boolean(value: bool | str, field_name: str, default_value: bool) -> bool:
            """
            Validates boolean
            """
            if isinstance(value, str):
                normalized_value = value.strip().lower()
                if normalized_value in {"true", "1", "yes"}:
                    return True
                elif normalized_value in {"false", "0", "no"}:
                    return False
            custom_console.bot_error_log(
                f"-> not configured {field_name} '{value}' Please use the default: {default_value}"
            )
            Config.wait_for_user_confirmation()
            return default_value

        def validate_int(value: int | str, field_name: str, default_value: int) -> int:
            """
            Validates integer
            """
            try:
                return int(value)
            except (ValueError, TypeError):
                custom_console.bot_error_log(
                    f"-> not configured {field_name} '{value}' Please use the default: {default_value}"
                )
                Config.wait_for_user_confirmation()
                return default_value

        def validate_str(value: str | None, field_name: str, default_value: str | None) -> str | None:
            """
            Validates string
            """
            if isinstance(value, str) and value.strip():
                return value
            custom_console.bot_error_log(
                f"-> not configured {field_name} '{value}' Please use the default: {default_value}"
            )
            Config.wait_for_user_confirmation()
            return default_value

        def validate_iso3166(value: str | None, field_name: str, default_value: str | None) -> str | None:
            """
            Validates string
            """
            if isinstance(value, str) and value.strip():
                if ManageTitles.convert_iso(value):
                    return value
                if value.lower()=='all':
                    return value
            custom_console.bot_error_log(
                f"-> not configured {field_name} '{value}' Please use the default: {default_value}"
            )
            Config.wait_for_user_confirmation()
            return default_value

        def validate_url(value: str, field_name: str, default_value: str) -> str:
            """
            Validates URL
            """
            if not value:
                return default_value
            parsed_url = urlparse(value)
            if not (parsed_url.scheme and parsed_url.netloc) or parsed_url.scheme not in ["http", "https"]:
                custom_console.bot_error_log(
                    f"->  Invalid URL value for {field_name} '{value}'. Use the default: {default_value}"
                )
                return default_value
            return value

        def validate_ip(value: str, field_name: str, default_value: str) -> str:
            """
            Validates IP address
            """
            if not value:
                return default_value
            try:
                parsed_ip = ipaddress.ip_address(value)
                return value
            except ValueError:
                custom_console.bot_error_log(
                    f"->  Invalid IP address value for {field_name} '{value}'. Use the default: {default_value}"
                )
                return default_value


        def validate_torrent_archive_path(value: str | None, field_name: str, default_value: str | None) -> str | None:
            """
            Validates path
            """
            if value is None or not isinstance(value, str) or not value.strip():
                return default_value
            path = Path(value).expanduser()
            if path.is_dir():
                return str(path)
            custom_console.bot_error_log(
                f"-> Invalid path for {field_name} '{value}' Please use the default: {default_value}"
            )
            Config.wait_for_user_confirmation()
            return default_value

        #// Mandatory
        values["ITT_URL"] = validate_url(values.get("ITT_URL", "https://itatorrents.xyz"), "ITT_URL", "https://itatorrents.xyz")
        values["PW_URL"] = validate_url(values.get("PW_URL", "http://localhost:9696/api/v1"), "PW_URL", "http://localhost:9696/api/v1")
        values["QBIT_USER"] = validate_str(values.get("QBIT_USER", None), "QBIT_USER", "admin")
        values["QBIT_PASS"] = validate_str(values.get("QBIT_PASS", None), "QBIT_PASS", "")
        values["QBIT_HOST"] = validate_ip(values.get("QBIT_HOST", "127.0.0.1"), "QBIT_HOST", "127.0.0.1")
        values["QBIT_PORT"] = validate_str(values.get("QBIT_PORT", "8080"), "QBIT_PORT", "8080")

        values["TRASM_USER"] = validate_str(values.get("TRASM_USER", None), "TRASM_USER", "admin")
        values["TRASM_PASS"] = validate_str(values.get("TRASM_PASS", None), "TRASM_PASS", "")
        values["TRASM_HOST"] = validate_ip(values.get("TRASM_HOST", "127.0.0.1"), "TRASM_HOST", "127.0.0.1")
        values["TRASM_PORT"] = validate_str(values.get("TRASM_PORT", "8080"), "TRASM_PORT", "8080")
        values["TORRENT_CLIENT"] = validate_str(values.get("TORRENT_CLIENT", "qbittorrent"), "TORRENT_CLIENT", "qbittorrent")

        values["ITT_APIKEY"] = validate_str(values.get("ITT_APIKEY", None), "ITT_APIKEY", None)
        values["TMDB_APIKEY"] = validate_str(values.get("TMDB_APIKEY", None), "TMDB_APIKEY", None)
        values["IMGBB_KEY"] = validate_str(values.get("IMGBB_KEY", None), "IMGBB_KEY", None)
        values["FREE_IMAGE_KEY"] = validate_str(values.get("FREE_IMAGE_KEY", None), "FREE_IMAGE_KEY", None)
        values["LENSDUMP_KEY"] = validate_str(values.get("LENSDUMP_KEY", None), "LENSDUMP_KEY", None)
        values["PTSCREENS_KEY"] = validate_str(values.get("PTSCREENS_KEY", None), "PTSCREENS_KEY", None)
        values["IMGFI_KEY"] = validate_str(values.get("IMGFI_KEY", None), "IMGFI_KEY", None)
        values["YOUTUBE_KEY"] = validate_str(values.get("YOUTUBE_KEY", None), "YOUTUBE_KEY", None)

        #// Preferences
        values["DUPLICATE_ON"] = validate_boolean(values.get("DUPLICATE_ON", False), "DUPLICATE_ON", False)
        values["SKIP_DUPLICATE"] = validate_boolean(values.get("SKIP_DUPLICATE", False), "SKIP_DUPLICATE", False)
        values["NUMBER_OF_SCREENSHOTS"] = validate_int(values.get("NUMBER_OF_SCREENSHOTS", 6), "NUMBER_OF_SCREENSHOTS", 6)
        values["COMPRESS_SCSHOT"] = validate_int(values.get("COMPRESS_SCSHOT", 4), "COMPRESS_SCSHOT", 4)
        values["RESIZE_SCSHOT"] = validate_boolean(values.get("RESIZE_SCSHOT", False), "RESIZE_SCSHOT", False)
        values["PREFERRED_LANG"] =  validate_iso3166(values.get("PREFERRED_LANG", None), "PREFERRED_LANG", "all")
        values["SIZE_TH"] = validate_int(values.get("SIZE_TH", 10), "SIZE_TH", 10)
        values["ANON"] = validate_boolean(values.get("ANON", False), "ANON", False)
        values["CACHE_SCR"] = validate_boolean(values.get("CACHE_SCR", False), "CACHE_SCR", False)

        values["TORRENT_COMMENT"] = validate_str(values.get("TORRENT_COMMENT", None), "TORRENT_COMMENT", "no_comment")
        values["TORRENT_ARCHIVE"] = validate_torrent_archive_path(values.get("TORRENT_ARCHIVE", None), "TORRENT_ARCHIVE", ".")
        values["PW_TORRENT_ARCHIVE_PATH"] = validate_str(values.get("PW_TORRENT_ARCHIVE_PATH", None), "PW_TORRENT_ARCHIVE_PATH", '.')
        values["PW_DOWNLOAD_PATH"] = validate_torrent_archive_path(values.get("PW_DOWNLOAD_PATH", None), "PW_DOWNLOAD_PATH", '.')
        values["WATCHER_DESTINATION_PATH"] = validate_torrent_archive_path(values.get("WATCHER_DESTINATION_PATH", None), "WATCHER_DESTINATION_PATH", '.')
        values["IMGBB_PRIORITY"] = validate_int(values.get("IMGBB_PRIORITY", 0), "IMGBB_PRIORITY", 0)
        values["FREE_IMAGE_PRIORITY"] = validate_int(values.get("FREE_IMAGE_PRIORITY", 1), "FREE_IMAGE_PRIORITY", 1)
        values["LENSDUMP_PRIORITY"] = validate_int(values.get("LENSDUMP_PRIORITY", 2), "LENSDUMP_PRIORITY", 2)
        values["WATCHER_PATH"] = validate_str(values.get("WATCHER_PATH", None), "WATCHER_PATH", "watcher_path")
        values["WATCHER_INTERVAL"] = validate_int(values.get("WATCHER_INTERVAL", 60), "WATCHER_INTERVAL", 60)

        values["YOUTUBE_FAV_CHANNEL_ID"] = validate_str(values.get("YOUTUBE_FAV_CHANNEL_ID", "UCGCbxpnt25hWPFLSbvwfg_w"),
                                                       "YOUTUBE_FAV_CHANNEL_ID", "UCGCbxpnt25hWPFLSbvwfg_w")

        values["YOUTUBE_CHANNEL_ENABLE"] = validate_boolean(values.get("YOUTUBE_CHANNEL_ENABLE", False),
                                                      "YOUTUBE_CHANNEL_ENABLE", False)

        #// Optional working in progress...
        values["PW_API_KEY"] = validate_str(values.get("PW_API_KEY", None), "PW_API_KEY", "no_key")
        values["PW_URL"] = validate_url(values.get("PW_URL", "http://localhost:9696/api/v1"), "PW_URL",
                                        "http://localhost:9696/api/v1")

        #// Optional
        values["FTPX_USER"] = validate_str(values.get("FTPX_USER", None), "FTPX_USER", "user")
        values["FTPX_PASS"] = validate_str(values.get("FTPX_PASS", None), "FTPX_PASS", "pass")
        values["FTPX_IP"] = validate_str(values.get("FTPX_IP", None), "FTPX_IP", "127.0.0.1")
        values["FTPX_PORT"] = validate_str(values.get("FTPX_PORT", "2121"), "FTPX_PORT", "2121")
        values["FTPX_LOCAL_PATH"] = validate_str(values.get("FTPX_LOCAL_PATH", None), "FTPX_LOCAL_PATH", ".")
        values["FTPX_ROOT"] = validate_str(values.get("FTPX_ROOT", "."), "FTPX_ROOT", ".")
        values["FTPX_KEEP_ALIVE"] = validate_boolean(values.get("FTPX_KEEP_ALIVE", False), "FTPX_KEEP_ALIVE", False)

        values["IGDB_CLIENT_ID"] = validate_str(values.get("IGDB_CLIENT_ID", None), "IGDB_CLIENT_ID", "client_id")
        values["IGDB_ID_SECRET"] = validate_str(values.get("IGDB_ID_SECRET", None), "IGDB_ID_SECRET", "secret")
        return values


@cache
def load_config():
    config = Config()
    return config


