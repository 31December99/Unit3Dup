# -*- coding: utf-8 -*-

from unit3dup.media_manager.utility import UserContent
from common.custom_console import custom_console
from common.utility.utility import ManageTitles
from common.trackers.trackers import ITTData
from common.config import load_config
from common.command import CommandLine

from tests.content_list import contents

# load the configuration
config = load_config()

# Load the argparse flags
cli = CommandLine()

# Load the tracker data from the dictionary
tracker_data = ITTData.load_from_module()

# force the uploader to set the media type as -movie, -serie, -game
force_media = None # tracker_data.category.get("game")

# /* ----------------------------------------------------------------------------------------------- */
custom_console.bot_warning_log("Pytest")

class Contents:

    def __init__(self, guess_title: str, category: int):
        self.guess_title = guess_title
        self.category = category


def test_tmdb_search_list():
    for content in contents:
        tmdb = UserContent.tmdb2(content=content)
        if tmdb:
            print(tmdb.get_title())
            assert  ManageTitles.fuzzyit(str1=tmdb.get_title(), str2=content.guess_title) > 95


