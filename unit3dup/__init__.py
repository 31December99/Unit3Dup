# -*- coding: utf-8 -*-
from unit3dup.config.bot_config import BotConfig
from unit3dup.shared.utility import System

from unit3dup.application.ContentManager import ContentManager
from unit3dup.application.user_content import UserContent

from unit3dup.external.torrent.bittorrent import BittorrentData
from unit3dup.external.theMovieDB.core.api import DbOnline
from unit3dup.external.theMovieDB.core.api import DbOnline
from unit3dup.external.torrent.pvtTorrent import Mytorrent
from unit3dup.external.media_files.tags import SearchTags
from unit3dup.external.video.pvtVideo import Video
from unit3dup.external.upload import UploadBot
from unit3dup.external.media import Media

from unit3dup.view import custom_console
from unit3dup.config.settings import Load

config_settings = Load().config

__all__ = [
    "config_settings",
    "ContentManager",
    "DbOnline",
    "Mytorrent",
    "BittorrentData",
    "BotConfig",
    "SearchTags",
    "System",
    "UserContent",
    "UploadBot",
    "Video",
    "Media",
    "custom_console",
]
