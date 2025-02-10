# -*- coding: utf-8 -*-
import argparse

from common.external_services.theMovieDB.core.models.tvshow.tvshow import TvShow
from common.external_services.theMovieDB.core.models.movie.movie import Movie
from common.external_services.theMovieDB.core.api import DbOnline
from common.custom_console import custom_console
from common.trackers.trackers import ITTData
from common.command import CommandLine
from common.config import load_config

from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.bot import Bot

# load the configuration
config = load_config()
# Load the argparse flags
cli = CommandLine()
# Load the tracker data from the dictionary
tracker_data = ITTData.load_from_module()

# /* ----------------------------------------------------------------------------------------------- */
force_media = 0

def test_cli_watcher():
    cli_scan = argparse.Namespace(
        tracker="itt",
        watcher=True,
        torrent=False,
        duplicate=False,
    )

    cli.args = cli_scan
    bot = Bot(
        path=r"",  # /**/
        tracker_name='itt',
        cli=cli.args,
        mode="auto"
    )
    assert bot.watcher(duration=config.WATCHER_INTERVAL, watcher_path=config.WATCHER_PATH,
                destination_path=config.WATCHER_DESTINATION_PATH, force_media_type=force_media) == True


def test_content_manager():

    test_content_movie = r"C:\test_folder\tvshow"
    content_manager = ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                     force_media_type=tracker_data.category.get("tvshow"))
    contents = content_manager.process()
    custom_console.bot_warning_log("\n- TVSHOW -")
    for content in contents:
        custom_console.bot_log(f"Display Name  {content.display_name}")
        custom_console.bot_log(f"Category      {content.category}")
        custom_console.bot_log(f"FileName      {content.file_name}")
        custom_console.bot_log(f"Folder        {content.folder}")
        custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        custom_console.bot_log(f"Resolution    {content.resolution}")
        custom_console.rule()


    test_content_game = r"C:\test_folder\games"
    content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tracker_data.category.get("game"))
    custom_console.bot_warning_log("- GAMES -")
    contents = content_manager.process()
    for content in contents:
        custom_console.bot_log(f"Display Name  {content.display_name}")
        custom_console.bot_log(f"Category      {content.category}")
        custom_console.bot_log(f"FileName      {content.file_name}")
        custom_console.bot_log(f"Folder        {content.folder}")
        custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        custom_console.bot_log(f"Resolution    {content.resolution}")
        custom_console.rule()


    custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tracker_data.category.get("movie"))
    contents = content_manager.process()
    for content in contents:
        custom_console.bot_log(f"Display Name  {content.display_name}")
        custom_console.bot_log(f"Category      {content.category}")
        custom_console.bot_log(f"FileName      {content.file_name}")
        custom_console.bot_log(f"Folder        {content.folder}")
        custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        custom_console.bot_log(f"Resolution    {content.resolution}")
        custom_console.rule()


def test_tmdb_search_list():
    custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tracker_data.category.get("movie"))
    contents = content_manager.process()


    for content in contents:
        # Search for the TMDB ID
        db_online = DbOnline(query=content.guess_title, category=content.category)
        tmdb = db_online.media_result
        if tmdb:
            assert isinstance(tmdb.result, Movie) or isinstance(tmdb.result, TvShow)
            assert hasattr(tmdb.result, 'get_title'), f"tmdb.result 'get_title()' not found for {content.guess_title}"
