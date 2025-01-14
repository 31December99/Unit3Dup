# -*- coding: utf-8 -*-

import os
import sys

from common.custom_console import custom_console
from pydantic_settings import BaseSettings
from pydantic import model_validator
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path

service_filename = "Unit3Dbot_service.env"

def create_default_env_file(path: Path):
    """
    Creates a default configuration file if it doesn't already exist
    """
    default_content = """
################################################## CONFIG ###################################################
# TRACKER
ITT_URL=https://itatorrents.xyz
ITT_APIKEY=

# TMDB
TMDB_APIKEY=

# IMAGE UPLOADERS
IMGBB_KEY=
FREE_IMAGE_KEY=
LENSDUMP_KEY=

# TRAILERS
YOUTUBE_KEY=no_apikey

# IGDB
IGDB_CLIENT_ID=client_id
IGDB_ID_SECRET=secret

# QBITTORRENT CLIENT
QBIT_USER=
QBIT_PASS=
QBIT_URL=http://localhost
QBIT_PORT=8080

############################################## USER PREFERENCES ##############################################
# Image uploader priority. 0=first in list
IMGBB_PRIORITY=0
FREE_IMAGE_PRIORITY=1
LENSDUMP_PRIORITY=2

# Youtube favorite channel Trailers FilmsNow it
YOUTUBE_FAV_CHANNEL_ID=UCGCbxpnt25hWPFLSbvwfg_w

# Use the YouTube favorite Channel if it is enabled otherwise perform a global search
YOUTUBE_CHANNEL_ENABLE=False

# Search for possible candidates for duplicate files
# True = enabled ; False = disabled
DUPLICATE_ON=False


# Discard videos whose size deviates by more than the specified percentage (size_th) from the video in tracker
# delta(%) < SIZE_TH = duplicate
SIZE_TH=10

# Watch the folder watcher_path at regular intervals (watcher_interval)
# and move its contents to user_path and then upload it
WATCHER_PATH=watcher_path
WATCHER_INTERVAL=60

# Number of screenshots we create
NUMBER_OF_SCREENSHOTS=4

# Level of compression for screenshot (quality) 0 = Best quality
COMPRESS_SCSHOT=4

# Resize image before sending to image hosting 
# True = Resize ; False = No resize
RESIZE_SCSHOT=False

# Path for each torrent file created
TORRENT_ARCHIVE=.

# Torrent file comment (max 100 chars)
TORRENT_COMMENT=no_comment

# Preferred language. Discard videos with a language different from preferred_lang (default=all)
PREFERRED_LANG=all

# Hide your nickname (only the nick name)
ANON=False

# Active the cache for the screenshots
CACHE_SCR=False

#########################################
################  OPTIONAL  #############  
#########################################
# PW
PW_API_KEY=no_key
PW_URL=http://localhost:9696/api/v1

# FTPX 
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
    Class to manage the configuration and validation of environment vvariables
    """

    ITT_URL: str = "https://itatorrents.xyz"
    ITT_APIKEY: str | None = None

    TMDB_APIKEY: str | None = None
    IMGBB_KEY: str | None = None
    FREE_IMAGE_KEY: str | None = None
    LENSDUMP_KEY: str | None = None
    YOUTUBE_KEY: str | None = None

    PW_API_KEY: str | None = None
    PW_URL: str = "http://localhost:9696/api/v1"
    FTPX_USER: str | None = None
    FTPX_PASS: str | None = None
    FTPX_IP: str | None = None
    FTPX_PORT: str = "2121"
    IGDB_CLIENT_ID: str | None = None
    IGDB_ID_SECRET: str | None = None

    QBIT_USER: str | None = None
    QBIT_PASS: str | None = None
    QBIT_URL: str = "http://127.0.0.1"
    QBIT_PORT: str = "8080"

    IMGBB_PRIORITY: int = 0
    FREE_IMAGE_PRIORITY: int = 1
    LENSDUMP_PRIORITY: int = 2

    YOUTUBE_FAV_CHANNEL_ID: str | None = None
    YOUTUBE_CHANNEL_ENABLE: bool = False

    DUPLICATE_ON: bool = False
    NUMBER_OF_SCREENSHOTS: int = 6
    COMPRESS_SCSHOT: int = 4
    RESIZE_SCSHOT: bool = False
    ANON: bool = False
    CACHE_SCR: bool = False


    WATCHER_PATH: str | None = None
    WATCHER_INTERVAL: int = 60

    TORRENT_ARCHIVE: str | None = None
    TORRENT_COMMENT: str | None = None
    PREFERRED_LANG: str | None = None
    SIZE_TH: int = 100

    FTPX_LOCAL_PATH: str | None = None
    FTPX_ROOT: str = "."
    FTPX_KEEP_ALIVE: bool = False

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
                f"-> not configured {field_name} '{value}' Using default: {default_value}"
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
                    f"-> not configured {field_name} '{value}' Using default: {default_value}"
                )
                Config.wait_for_user_confirmation()
                return default_value

        def validate_str(value: str | None, field_name: str, default_value: str | None) -> str | None:
            """
            Validates strinng
            """
            if isinstance(value, str) and value.strip():
                return value
            custom_console.bot_error_log(
                f"-> not configured {field_name} '{value}' Using default: {default_value}"
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
            if not (parsed_url.scheme and parsed_url.netloc):
                custom_console.bot_error_log(
                    f"->  Invalid URL value for {field_name} '{value}' Using default: {default_value}"
                )
                return default_value
            return value


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
                f"-> Invalid path for {field_name} '{value}' Using default: {default_value}"
            )
            Config.wait_for_user_confirmation()
            return default_value

        #// Mandatory
        values["ITT_URL"] = validate_url(values.get("ITT_URL", "https://itatorrents.xyz"), "ITT_URL", "https://itatorrents.xyz")
        values["PW_URL"] = validate_url(values.get("PW_URL", "http://localhost:9696/api/v1"), "PW_URL", "http://localhost:9696/api/v1")
        values["QBIT_URL"] = validate_url(values.get("QBIT_URL", "http://127.0.0.1"), "QBIT_URL", "http://127.0.0.1")
        values["QBIT_USER"] = validate_str(values.get("QBIT_USER", None), "QBIT_USER", "admin")
        values["QBIT_PASS"] = validate_str(values.get("QBIT_PASS", None), "QBIT_PASS", "")
        values["QBIT_URL"] = validate_url(values.get("QBIT_URL", "http://127.0.0.1"), "QBIT_URL", "http://127.0.0.1")
        values["QBIT_PORT"] = validate_str(values.get("QBIT_PORT", "8080"), "QBIT_PORT", "8080")
        values["ITT_APIKEY"] = validate_str(values.get("ITT_APIKEY", None), "ITT_APIKEY", None)
        values["TMDB_APIKEY"] = validate_str(values.get("TMDB_APIKEY", None), "TMDB_APIKEY", None)
        values["IMGBB_KEY"] = validate_str(values.get("IMGBB_KEY", None), "IMGBB_KEY", None)
        values["FREE_IMAGE_KEY"] = validate_str(values.get("FREE_IMAGE_KEY", None), "FREE_IMAGE_KEY", None)
        values["LENSDUMP_KEY"] = validate_str(values.get("LENSDUMP_KEY", None), "LENSDUMP_KEY", None)
        values["YOUTUBE_KEY"] = validate_str(values.get("YOUTUBE_KEY", None), "YOUTUBE_KEY", None)

        #// Preferences
        values["DUPLICATE_ON"] = validate_boolean(values.get("DUPLICATE_ON", False), "DUPLICATE_ON", False)
        values["NUMBER_OF_SCREENSHOTS"] = validate_int(values.get("NUMBER_OF_SCREENSHOTS", 6), "NUMBER_OF_SCREENSHOTS", 6)
        values["COMPRESS_SCSHOT"] = validate_int(values.get("COMPRESS_SCSHOT", 4), "COMPRESS_SCSHOT", 4)
        values["RESIZE_SCSHOT"] = validate_boolean(values.get("RESIZE_SCSHOT", False), "RESIZE_SCSHOT", False)
        values["PREFERRED_LANG"] = validate_str(values.get("PREFERRED_LANG", None), "PREFERRED_LANG", "all")
        values["SIZE_TH"] = validate_int(values.get("SIZE_TH", 10), "SIZE_TH", 10)
        values["ANON"] = validate_boolean(values.get("ANON", False), "ANON", False)
        values["CACHE_SCR"] = validate_boolean(values.get("CACHE_SCR", False), "CACHE_SCR", False)

        values["TORRENT_COMMENT"] = validate_str(values.get("TORRENT_COMMENT", None), "TORRENT_COMMENT", "no_comment")
        values["TORRENT_ARCHIVE"] = validate_torrent_archive_path(values.get("TORRENT_ARCHIVE", None), "TORRENT_ARCHIVE", ".")
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

    @staticmethod
    def wait_for_user_confirmation():
        # Wait for user confirmation in case of validation failure
        try:
            custom_console.bot_log(
                "Press Enter to continue with the default value or Ctrl-C to exit and update your config file *.env")
            input()
        except KeyboardInterrupt:
            custom_console.bot_log("\nOperation cancelled.Please update your config file")
            sys.exit(0)

if os.name == "nt":
    # C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_\LocalCache\Local
    default_env_path: Path = Path(os.getenv("LOCALAPPDATA", ".")) / f"{service_filename}"
    torrent_archive_path: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "torrent_archive"
    default_env_path_cache: Path = Path(os.getenv("LOCALAPPDATA", ".")) / f"Unit3Dup_cache"
else:
    default_env_path: Path = Path.home() / f"{service_filename}"
    torrent_archive_path: Path = Path.home() / "torrent_archive"
    default_env_path_cache: Path = Path.home() / "Unit3Dup_cache"


if not default_env_path.exists():
    print(f"Create default configuration file: {default_env_path}\n")
    create_default_env_file(default_env_path)

if not torrent_archive_path.exists():
    print(f"Create default torrent archive path: {torrent_archive_path}")
    os.makedirs(torrent_archive_path, exist_ok=True)

if not default_env_path_cache.exists():
    print(f"Create default cache path: {default_env_path_cache}")
    os.makedirs(default_env_path_cache, exist_ok=True)


# /// Display welcome message
custom_console.welcome_message()
custom_console.bot_question_log(f"Checking your configuration file.. * {default_env_path} *\n")
load_dotenv(dotenv_path=default_env_path)

config = Config()
