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

# load the configuration
config = load_config()
# Load the argparse flags
cli = CommandLine()
# Load the tracker data from the dictionary
tracker_data = ITTData.load_from_module()


class Content:
    def __init__(self):
        pass

    @staticmethod
    def content()->list[Media]:


        # -scan
        custom_console.bot_warning_log("\n- TVSHOW -")
        test_content_movie = r"C:\test_folder\serie"
        content_manager = ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                               force_media_type=tracker_data.category.get("tvshow"))
        tvshow_list = content_manager.process()

        # -scan
        custom_console.bot_warning_log("- MOVIE -")
        test_content_game = r"C:\test_folder\movie"
        content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                               force_media_type=tracker_data.category.get("movie"))
        movie_list = content_manager.process()

        # -f
        custom_console.bot_warning_log("- FOLDER -")
        test_content_game = r"C:\test_folder\Andromeda.S01E01.Under.the.Night.1080p.AMZN.WEB-DL.DDP2.0.H265"
        content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='folder',
                                               force_media_type=tracker_data.category.get("tvshow"))
        folder_list = content_manager.process()


        custom_console.bot_warning_log("- SINGLE -")
        test_content_game = r"C:\test_folder\L'illusionista WEB-DL 1080p AC3 E-AC3 ITA SPA SUB-LF.mkv"
        content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='man',
                                               force_media_type=tracker_data.category.get("movie"))
        single_list = content_manager.process()


        return folder_list + tvshow_list + movie_list +  single_list
