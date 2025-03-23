# -*- coding: utf-8 -*-

import argparse
from common.torrent_clients import TransmissionClient, QbittorrentClient
from common.external_services.theMovieDB.core.api import DbOnline
from common.external_services.igdb.client import IGDBClient
from common.trackers.trackers import TRACKData
from common.mediainfo import MediaFile
from common.command import CommandLine
from common.settings import Load
from common.utility import System


from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup.pvtVideo import Video
from unit3dup.bot import Bot


from view import custom_console

cli = CommandLine()
config = Load.load_config()







