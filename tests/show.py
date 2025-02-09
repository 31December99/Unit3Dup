# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.core.models.movie.movie import Movie
from common.external_services.theMovieDB.core.models.tvshow.tvshow import TvShow
from common.external_services.theMovieDB.core.api import DbOnline
from common.custom_console import custom_console
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

# /* ----------------------------------------------------------------------------------------------- */
custom_console.bot_warning_log("Pytest")

class Contents:

    def __init__(self, guess_title: str, category: int):
        self.guess_title = guess_title
        self.category = category


def test_tmdb_search_list():
    for content in contents:
        # Search for the TMDB ID
        db_online = DbOnline(query=content.guess_title, category=content.category)
        tmdb = db_online.media_result
        if tmdb:
            assert isinstance(tmdb.result, Movie) or isinstance(tmdb.result, TvShow)
            assert hasattr(tmdb.result, 'get_title'), f"tmdb.result 'get_title()' not found for {content.guess_title}"
