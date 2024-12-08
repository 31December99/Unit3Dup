# -*- coding: utf-8 -*-

import os
from common.custom_console import custom_console
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path

service_filename = "Unit3Dbot_service.env"

def create_default_env_file(path):
    default_content = """
################################################## CONFIG ###################################################
# TRACKER
ITT_URL=https://itatorrents.xyz
ITT_APIKEY=

# TMDB
TMDB_APIKEY=

# IMGBB;FREE_IMAGE
IMGBB_KEY=
FREE_IMAGE_KEY=

# QBITTORRENT CLIENT
QBIT_USER=
QBIT_PASS=
QBIT_URL=http://localhost
QBIT_PORT=8080

############################################## USER PREFERENCES ##############################################

# Image uploader priority. 1=first in list
IMGBB_PRIORITY=1
FREE_IMAGE_PRIORITY=2

# Search for possible candidates for duplicate files
DUPLICATE_ON=False

# Number of screenshots we create
NUMBER_OF_SCREENSHOTS=6

# Level of compression for screenshot (quality) 0 = Best quality
COMPRESS_SCSHOT=4

# Path for each torrent file created
TORRENT_ARCHIVE=

# Torrent file comment (max 100 chars)
TORRENT_COMMENT=

# Preferred language. Discard videos with a language different from preferred_lang
PREFERRED_LANG=

# Discard videos whose size deviates by more than the specified percentage (size_th) from the video in tracker
SIZE_TH=100


##############################################################################################################
################  OPTIONAL  #############  
#########################################
# PW
PW_API_KEY=
PW_URL=http://localhost:9696/api/v1

# FTPX 
FTPX_USER=
FTPX_PASS=
FTPX_IP=
FTPX_PORT=2121
FTPX_LOCAL_PATH= 
FTPX_ROOT=
FTPX_KEEP_ALIVE=False

# IGDB
IGDB_CLIENT_ID=
IGDB_ID_SECRET=
"""
    with open(path, "w") as f:
        f.write(default_content.strip())

# Define the path for the configuration file
if os.name == "nt":  # If on Windows
    default_env_path = Path(os.getenv("LOCALAPPDATA", ".")) / f"{service_filename}"
    torrent_archive_path = Path(os.getenv("LOCALAPPDATA", ".")) / "torrent_archive"
else:  # If on Linux/macOS
    default_env_path = Path.home() / f"{service_filename}"
    torrent_archive_path = Path.home() / "torrent_archive"

custom_console.bot_question_log(f"Default configuration path: {default_env_path}\n")

# Create the configuration file if it does not exist
if not default_env_path.exists():
    print(f"Create default configuration file: {default_env_path}")
    create_default_env_file(default_env_path)

# Create the directory for the torrent archive if it does not exist
if not torrent_archive_path.exists():
    print(f"Create default torrent archive path: {torrent_archive_path}")
    os.makedirs(torrent_archive_path, exist_ok=True)

# Load environment variables
load_dotenv(dotenv_path=default_env_path)

class Config(BaseSettings):
    # TRACKER
    ITT_APIKEY: str | None = Field(default=None, env="ITT_APIKEY")
    ITT_URL: str = Field(default="https://itatorrents.xyz", env="ITT_URL")

    # EXTERNAL SERVICE
    TMDB_APIKEY: str | None = Field(default=None, env="TMDB_APIKEY")
    IMGBB_KEY: str | None = Field(default=None, env="IMGBB_KEY")
    FREE_IMAGE_KEY: str | None = Field(default=None, env="FREE_IMAGE_KEY")
    PW_API_KEY: str | None = Field(default=None, env="PW_API_KEY")
    PW_URL: str = Field(default="http://localhost:9696/api/v1", env="PW_URL")
    FTPX_USER: str | None = Field(default=None, env="FTPX_USER")
    FTPX_PASS: str | None = Field(default=None, env="FTPX_PASS")
    FTPX_IP: str | None = Field(default=None, env="FTPX_IP")
    FTPX_PORT: str | None = Field(default="2121", env="FTPX_PORT")
    IGDB_CLIENT_ID: str | None = Field(default=None, env="IGDB_CLIENT_ID")
    IGDB_ID_SECRET: str | None = Field(default=None, env="IGDB_ID_SECRET")

    # TORRENT CLIENT
    QBIT_USER: str | None = Field(default=None, env="QBIT_USER")
    QBIT_PASS: str | None = Field(default=None, env="QBIT_PASS")
    QBIT_URL: str = Field(default="http://127.0.0.1", env="QBIT_URL")
    QBIT_PORT: str | None = Field(default="8080", env="QBIT_PORT")

    # USER PREFERENCES
    FREE_IMAGE_PRIORITY: int = Field(default=1, env="FREE_IMAGE_PRIORITY")
    IMGBB_PRIORITY: int = Field(default=2, env="IMGBB_PRIORITY")
    DUPLICATE_ON: str = Field(default=False, env="DUPLICATE_ON")
    NUMBER_OF_SCREENSHOTS: int = Field(default=6, env="NUMBER_OF_SCREENSHOTS")
    COMPRESS_SCSHOT: int = Field(default=4, env="COMPRESS_SCSHOT")
    TORRENT_ARCHIVE: str | None = Field(default=None, env="TORRENT_ARCHIVE")
    TORRENT_COMMENT: str | None = Field(default=None, env="TORRENT_COMMENT")
    PREFERRED_LANG: str | None = Field(default=None, env="PREFERRED_LANG")
    SIZE_TH: int = Field(default=100, env="SIZE_TH")
    FTPX_LOCAL_PATH: str | None = Field(default=None, env="FTPX_LOCAL_PATH")
    FTPX_ROOT: str | None = Field(default=".", env="FTPX_ROOT")
    FTPX_KEEP_ALIVE: bool | None = Field(default=False, env="FTPX_KEEP_ALIVE")

    def __init__(self, **values: any):
        super().__init__(**values)

    @staticmethod
    def validate_url(value: str | None, field: str, fields: dict) -> str:
        if not value:
            return fields[field].default
        parsed_url = urlparse(value)
        if not (parsed_url.scheme and parsed_url.netloc):
            custom_console.bot_error_log(
                f"{value} is an invalid URL. Using default: {fields[field].default}"
            )
            return fields[field].default
        return value

    @staticmethod
    def validate_boolean(value: any, field: str, fields: dict) -> bool:
        if isinstance(value, str):
            lowered_value = value.lower()
            if lowered_value in ["true", "1", "yes"]:
                return True
            elif lowered_value in ["false", "0", "no"]:
                return False
        custom_console.bot_error_log(
            f"{value} is not a valid boolean for {field}. Using default: {fields[field].default}"
        )
        return fields[field].default

    @field_validator("ITT_URL")
    def validate_itt_url(cls, value):
        if not value:
            custom_console.bot_error_log("No ITT_URL provided")
        return cls.validate_url(value, "ITT_URL", cls.model_fields)

    @field_validator("ITT_APIKEY")
    def validate_itt_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No ITT_APIKEY provided")
        return value

    @field_validator("QBIT_URL")
    def validate_qbit_url(cls, value):
        if not value:
            custom_console.bot_error_log("No QBIT_URL provided")
        return cls.validate_url(value, "QBIT_URL", cls.model_fields)

    @field_validator("PW_URL")
    def validate_pw_url(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No PW_URL provided\n")
        return cls.validate_url(value, "PW_URL", cls.model_fields)

    @field_validator("PW_API_KEY")
    def validate_pw_apikey(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No PW_API_KEY provided\n")
        return value

    @field_validator("TMDB_APIKEY")
    def validate_tmdb_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No TMDB API_KEY provided")
        return value

    @field_validator("IMGBB_KEY")
    def validate_imgbb_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No IMGBB API_KEY provided")
        return value

    @field_validator("FREE_IMAGE_KEY")
    def validate_freeimage_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No FREE IMAGE API_KEY provided")
        return value

    @field_validator("QBIT_USER")
    def validate_qbit_user(cls, value):
        if not value:
            custom_console.bot_error_log("No QBIT_USER provided")
        return value

    @field_validator("QBIT_PASS")
    def validate_qbit_pass(cls, value):
        if not value:
            custom_console.bot_error_log("No QBIT_PASS provided")
        return value

    @field_validator("QBIT_PORT")
    def validate_qbit_port(cls, value):
        if not value:
            custom_console.bot_error_log("No QBIT_PORT provided")
        return value

    @field_validator("FREE_IMAGE_PRIORITY")
    def validate_free_image_priority(cls, value):
        if not isinstance(value, int) or not (1 <= value <= 2):
            return cls.model_fields["FREE_IMAGE_PRIORITY"].default
        return value

    @field_validator("IMGBB_PRIORITY")
    def validate_imgbb_priority(cls, value):
        if not isinstance(value, int) or not (1 <= value <= 2):
            return cls.model_fields["IMGBB_PRIORITY"].default
        return value

    @field_validator("DUPLICATE_ON")
    def validate_duplicate_on(cls, value):
        return cls.validate_boolean(value, "DUPLICATE_ON", cls.model_fields)

    @field_validator("NUMBER_OF_SCREENSHOTS")
    def validate_n_screenshot(cls, value):
        if not isinstance(value, int) or not (3 <= value <= 10):
            return cls.model_fields["NUMBER_OF_SCREENSHOTS"].default
        return value

    @field_validator("COMPRESS_SCSHOT")
    def validate_compress_sc_shot(cls, value):
        if not isinstance(value, int) or not (0 <= value <= 10):
            return cls.model_fields["COMPRESS_SCSHOT"].default
        return value

    @field_validator("TORRENT_ARCHIVE")
    def validate_torrent_archive(cls, value):
        if not isinstance(value, str):
            return cls.model_fields["TORRENT_ARCHIVE"].default
        return value

    @field_validator("TORRENT_COMMENT")
    def validate_torrent_comment(cls, value):
        if not isinstance(value, str):
            return cls.model_fields["TORRENT_COMMENT"].default
        return value

    @field_validator("PREFERRED_LANG")
    def validate_preferred_lang(cls, value):
        if not isinstance(value, str):
            return cls.model_fields["PREFERRED_LANG"].default
        return value

    @field_validator("SIZE_TH")
    def validate_size_th(cls, value):
        if not isinstance(value, int) or value <= 0:
            return cls.model_fields["SIZE_TH"].default
        return value

    @field_validator("FTPX_USER")
    def validate_ftpx_user(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_USER provided\n")
        return value

    @field_validator("FTPX_PASS")
    def validate_ftpx_pass(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_PASS provided\n")
        return value

    @field_validator("FTPX_IP")
    def validate_ftpx_ip(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_IP provided\n")
        return value

    @field_validator("FTPX_PORT")
    def validate_ftpx_port(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_PORT provided\n")
        return value

    @field_validator("FTPX_LOCAL_PATH")
    def validate_ftpx_local_path(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_LOCAL_PATH provided\n")
        return value

    @field_validator("FTPX_ROOT")
    def validate_ftpx_root(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No FTPX_ROOT folder provided\n")
        return value

    @field_validator("IGDB_CLIENT_ID")
    def validate_igdb_client_id(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No IGDB_CLIENT_ID provided\n")
        return value

    @field_validator("IGDB_ID_SECRET")
    def validate_igdb_id_secret(cls, value):
        # if not value:
        # custom_console.bot_question_log("[Optional] No IGDB_ID_SECRET provided\n")
        return value


config = Config()
