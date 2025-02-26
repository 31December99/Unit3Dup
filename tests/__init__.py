# -*- coding: utf-8 -*-

import argparse

from common.external_services.theMovieDB.core.models.tvshow.tvshow import TvShow
from common.external_services.theMovieDB.core.models.movie.movie import Movie
from common.external_services.theMovieDB.core.api import DbOnline

from common.torrent_clients import TransmissionClient, QbittorrentClient
from common.custom_console import custom_console
from common.bittorrent import BittorrentData
from common.trackers.trackers import ITTData
from common.command import CommandLine
from common.mediainfo import MediaFile
from common.config import load_config

from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
from unit3dup.bot import Bot

