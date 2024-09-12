# -*- coding: utf-8 -*-

import os
from common.custom_console import custom_console
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path


def create_default_env_file(path):
    default_content = """
# TRACKER
ITT_URL=https://itatorrents.xyz
ITT_APIKEY=

# EXTERNAL SERVICE
TMDB_APIKEY=
IMGBB_KEY=
FREE_IMAGE_KEY=
PW_API_KEY=
PW_URL=http://localhost:9696/api/v1

# TORRENT CLIENT
QBIT_USER=
QBIT_PASS=
QBIT_URL=http://localhost:8080
QBIT_PORT=

# USER PREFERENCES
DUPLICATE_ON=False
NUMBER_OF_SCREENSHOTS=6
COMPRESS_SCSHOT=4
TORRENT_ARCHIVE=
PREFERRED_LANG=
SIZE_TH=100
"""
    with open(path, "w") as f:
        f.write(default_content.strip())


# Define the path for the configuration file ( Windows/Linux)
if os.name == "nt":
    default_env_path = Path(os.getenv("APPDATA", ".")) / "service.env"
    torrent_archive_path = Path(os.getenv("APPDATA", ".")) / "torrent_archive"
else:
    default_env_path = Path.home() / "service.env"
    torrent_archive_path = Path.home() / "torrent_archive"

# print the configuration path
custom_console.bot_log(f"Default configuration path... {default_env_path}")

# Create the configuration file if it does not exist
if not default_env_path.exists():
    custom_console.bot_log(f"Create default configuration file... {default_env_path}")
    create_default_env_file(default_env_path)

# Create the directory for the torrent archive if it does not exist
if not torrent_archive_path.exists():
    custom_console.bot_log(
        f"Create default torrent archive path... {torrent_archive_path}"
    )
    os.makedirs(torrent_archive_path, exist_ok=True)

# Load environment variables
load_dotenv(dotenv_path=default_env_path)


class Config(BaseSettings):
    # TRACKER
    ITT_APIKEY: str | None = Field(default=None, env="ITT_APIKEY")
    ITT_URL: str | None = Field(default=None, env="ITT_URL")

    # EXTERNAL SERVICE
    TMDB_APIKEY: str | None = Field(default=None, env="TMDB_APIKEY")
    IMGBB_KEY: str | None = Field(default=None, env="IMGBB_KEY")
    FREE_IMAGE_KEY: str | None = Field(default=None, env="FREE_IMAGE_KEY")
    PW_API_KEY: str | None = Field(default=None, env="PW_API_KEY")
    PW_URL: str = Field(default="http://localhost:9696/api/v1", env="PW_URL")

    # TORRENT CLIENT
    QBIT_USER: str | None = Field(default=None, env="QBIT_USER")
    QBIT_PASS: str | None = Field(default=None, env="QBIT_PASS")
    QBIT_URL: str = Field(default="http://localhost:8080", env="QBIT_URL")
    QBIT_PORT: str | None = Field(default="8080", env="QBIT_PORT")

    # USER PREFERENCES
    DUPLICATE_ON: bool = Field(default=False, env="DUPLICATE_ON")
    NUMBER_OF_SCREENSHOTS: int = Field(default=6, env="NUMBER_OF_SCREENSHOTS")
    COMPRESS_SCSHOT: int = Field(default=4, env="COMPRESS_SCSHOT")
    TORRENT_ARCHIVE: str | None = Field(default=None, env="TORRENT_ARCHIVE")
    PREFERRED_LANG: str | None = Field(default=None, env="PREFERRED_LANG")
    SIZE_TH: int = Field(default=100, env="SIZE_TH")

    def __init__(self, **values: any):
        super().__init__(**values)

    @staticmethod
    def validate_url(value: str | None, default_value: str) -> str:
        if not value:
            return default_value
        parsed_url = urlparse(value)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError(f"{value} Invalid Url")
        return value

    @field_validator("ITT_URL")
    def validate_itt_url(cls, value):
        if not value:
            custom_console.bot_error_log("No ITT_URL provided")
        return cls.validate_url(value, cls.__fields__["ITT_URL"].default)

    @field_validator("ITT_APIKEY")
    def validate_itt_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No ITT_APIKEY provided")
        return value

    @field_validator("QBIT_URL")
    def validate_qbit_url(cls, value):
        if not value:
            custom_console.bot_error_log("No QBIT_URL provided")
        return cls.validate_url(value, cls.__fields__["QBIT_URL"].default)

    @field_validator("PW_URL")
    def validate_pw_url(cls, value):
        if not value:
            custom_console.bot_error_log("No PW_URL provided")
        return cls.validate_url(value, cls.__fields__["PW_URL"].default)

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

    @field_validator("PW_API_KEY")
    def validate_pw_apikey(cls, value):
        if not value:
            custom_console.bot_error_log("No PW API_KEY provided")
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

    @field_validator("DUPLICATE_ON")
    def validate_duplicate_on(cls, value):
        if not isinstance(value, bool):
            custom_console.bot_error_log("DUPLICATE_ON should be a boolean")
            return cls.__fields__["DUPLICATE_ON"].default
        return value

    @field_validator("NUMBER_OF_SCREENSHOTS")
    def validate_n_screenshot(cls, value):
        if not isinstance(value, int) or not (3 <= value <= 10):
            return cls.__fields__["NUMBER_OF_SCREENSHOTS"].default
        return value

    @field_validator("COMPRESS_SCSHOT")
    def validate_compress_sc_shot(cls, value):
        if not isinstance(value, int) or not (0 <= value <= 10):
            return cls.__fields__["COMPRESS_SCSHOT"].default
        return value

    @field_validator("TORRENT_ARCHIVE")
    def validate_torrent_archive(cls, value):
        if not isinstance(value, str):
            return cls.__fields__["TORRENT_ARCHIVE"].default
        return value

    @field_validator("PREFERRED_LANG")
    def validate_preferred_lang(cls, value):
        if not isinstance(value, str):
            return cls.__fields__["PREFERRED_LANG"].default
        return value

    @field_validator("SIZE_TH")
    def validate_size_th(cls, value):
        if not isinstance(value, int) or value <= 0:
            return cls.__fields__["SIZE_TH"].default
        return value


config = Config()
