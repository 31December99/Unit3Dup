# -*- coding: utf-8 -*-
import json

from unit3dup.common.settings import Load, DEFAULT_JSON_PATH, USER_TAGS_PATH, USER_SIGN_PATH, BAN_TAGS_PATH, version
from unit3dup.common.torrent_clients import TransmissionClient, QbittorrentClient, RTorrentClient
from unit3dup.common.command import CommandLine
from unit3dup.common.bot_config import BotConfig

from unit3dup.torrent import View
from unit3dup import pvtTracker
from unit3dup.bot import Bot
from unit3dup.view import custom_console


def main():
    """
    Main function to handle the command line interface (CLI)
    """

    custom_console.welcome_message()
    custom_console.bot_question_log(f"Unit3Dup {version} Checking your configuration file.. \n")

    # Load user configuration data
    config = Load().load_config()
    custom_console.bot_log(f"[Configuration] '{DEFAULT_JSON_PATH}'")
    custom_console.bot_log(f"[*.torrent Archive] '{config.user_preferences.TORRENT_ARCHIVE_PATH}'")
    custom_console.bot_log(f"[Images,Tmdb cache] '{config.user_preferences.CACHE_PATH}'")
    custom_console.bot_log(f"[Watcher] '{config.user_preferences.WATCHER_PATH}'")
    custom_console.bot_log(f"[Watcher] '{config.user_preferences.WATCHER_DESTINATION_PATH}'")
    custom_console.bot_log(f"[Preferred Language] '{config.user_preferences.PREFERRED_LANG}'")
    custom_console.bot_log(f"[Youtube Preferred Language] '{config.user_preferences.YOUTUBE_PREF_LANG}'")
    print()

    # /// Initialize command line interface
    user = CommandLine()

    # /// Decoupling user args from the cli namespace
    cli = BotConfig.from_namespace(user.args)

    # Get the torrent archive path
    if config.user_preferences.TORRENT_ARCHIVE_PATH:
        tracker_archive = config.user_preferences.TORRENT_ARCHIVE_PATH
    else:
        tracker_archive = '.'

    # /// Load the list of the registered trackers
    if not config.tracker_config.MULTI_TRACKER:
        custom_console.bot_error_log(f"No tracker name provided. Please update your configuration file")
        exit(1)

    # Check if the tracker name exists
    if cli.tracker:
        if not any(cli.tracker.upper() in tracker.upper() for tracker in config.tracker_config.MULTI_TRACKER):
            custom_console.bot_error_log(
                f"Tracker '{cli.tracker}' not found. Please update your configuration file")
            exit()

        tracker = pvtTracker.Unit3d(tracker_name=cli.tracker)
        if tracker.get_alive(alive=True, perPage=1):
            custom_console.bot_log(f"Tracker -> '{cli.tracker.upper()}' Online")
            tracker_name_list = [cli.tracker.upper()]

    # Send content to the multi_tracker list
    if cli.mt:
        tracker_name_list = config.tracker_config.MULTI_TRACKER
        for tracker_data in tracker_name_list[1:]:
            tracker = pvtTracker.Unit3d(tracker_name=tracker_data)
            if tracker.get_alive(alive=True, perPage=1):
                custom_console.bot_log(f"Tracker -> '{tracker_data.upper()}' Online")

    # Test both clients only if used
    if cli.noseed is False and cli.noup is False or cli.reseed is True:
        # /// Test the torrent clients
        if cli.scan or cli.upload or cli.folder or cli.watcher:
            if config.torrent_client_config.TORRENT_CLIENT.lower() == "qbittorrent":
                test_client_torrent = QbittorrentClient()
                if not test_client_torrent.connect():
                    exit(1)
            elif config.torrent_client_config.TORRENT_CLIENT.lower() == "transmission":
                test_client_torrent = TransmissionClient()
                if not test_client_torrent.connect():
                    exit(1)

            elif config.torrent_client_config.TORRENT_CLIENT.lower() == "rtorrent":
                test_client_torrent = RTorrentClient()
                if not test_client_torrent.connect():
                    exit(1)

            else:
                custom_console.bot_error_log(
                    f"Unknown Torrent Client name '{config.torrent_client_config.TORRENT_CLIENT}'")
                custom_console.bot_error_log(f"You need to set a favorite 'torrent_client' in the config file")
                exit(1)

    # Load User Tags list
    tags_list = None
    if cli.buildtags:
        try:
            with open(USER_TAGS_PATH, "r", encoding="utf-8") as f:
                tags_list = json.load(f)
        except FileNotFoundError:
            custom_console.bot_error_log(
                f"User tags file {USER_TAGS_PATH} not found. Please update your configuration file")

    # Load User Sign list
    sign_list = None
    try:
        with open(USER_SIGN_PATH, "r", encoding="utf-8") as f:
            sign_list = json.load(f)
    except FileNotFoundError:
        custom_console.bot_error_log(
            f"User sign file {USER_SIGN_PATH} not found. Please update your configuration file")

    # Load Ban list
    ban_list = None
    try:
        with open(BAN_TAGS_PATH, "r", encoding="utf-8") as f:
            ban_list = json.load(f)
    except FileNotFoundError:
        custom_console.bot_error_log(
            f"Ban list file {BAN_TAGS_PATH} not found. Please update your configuration file")

    # Manual upload mode
    if cli.upload:
        bot = Bot(path=cli.upload, cli=cli, trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive, tags_list=tags_list, sign_list=sign_list, ban_list=ban_list)
        bot.run()

    # Manual folder mode
    if cli.folder:
        bot = Bot(
            path=cli.folder,
            cli=cli,
            mode="folder",
            trackers_name_list=tracker_name_list,
            torrent_archive_path=tracker_archive,
            tags_list=tags_list,
            sign_list=sign_list,
            ban_list=ban_list
        )
        bot.run()

    # Auto mode
    if cli.scan and not cli.ftp:
        bot = Bot(path=cli.scan, cli=cli, mode="auto", trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive, tags_list=tags_list, sign_list=sign_list, ban_list=ban_list)
        bot.run()

    # Watcher
    if cli.watcher:
        bot = Bot(path='', cli=cli, mode="auto", trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive)

        bot.watcher(duration=config.user_preferences.WATCHER_INTERVAL,
                    watcher_path=config.user_preferences.WATCHER_PATH,
                    destination_path=config.user_preferences.WATCHER_DESTINATION_PATH)

    # ftp and upload
    if cli.ftp:
        bot = Bot(path='', cli=cli, mode="folder", trackers_name_list=tracker_name_list)
        bot.ftp()

    # Commands list: commands not necessary for upload but may be useful
    if not cli.tracker:
        return

    torrent_info = View(tracker_name=cli.tracker)

    ############################ Filter 'Combo' ##########################
    if cli.tmdb_id and cli.resolution:
        torrent_info.view_tmdb_res(cli.tmdb_id, cli.resolution)
        return
    #####################################################################

    # Search by different criteria
    if cli.search:
        torrent_info.view_search(cli.search, save=cli.dbsave)
        return

    # Dump
    if cli.dump:
        torrent_info.view_search(" ", inkey=False, save=True)
        return

    if cli.info:
        torrent_info.view_search(cli.info, info=True)
        return

    if cli.description:
        torrent_info.view_by_description(cli.description)
        return

    if cli.bdinfo:
        torrent_info.view_by_bdinfo(cli.bdinfo)
        return

    if cli.uploader:
        torrent_info.view_by_uploader(cli.uploader, save=cli.dbsave)
        return

    if cli.startyear:
        torrent_info.view_by_start_year(cli.startyear)
        return

    if cli.endyear:
        torrent_info.view_by_end_year(cli.endyear)
        return

    if cli.type:
        torrent_info.view_by_types(cli.type)
        return

    if cli.resolution:
        torrent_info.view_by_res(cli.resolution)
        return

    if cli.filename:
        torrent_info.view_by_filename(cli.filename)
        return

    if cli.tmdb_id:
        torrent_info.view_by_tmdb_id(cli.tmdb_id)
        return

    if cli.imdb_id:
        torrent_info.view_by_imdb_id(cli.imdb_id)
        return

    if cli.tvdb_id:
        torrent_info.view_by_tvdb_id(cli.tvdb_id)
        return

    if cli.mal_id:
        torrent_info.view_by_mal_id(cli.mal_id)
        return

    if cli.playlist_id:
        torrent_info.view_by_playlist_id(cli.playlist_id)
        return

    if cli.collection_id:
        torrent_info.view_by_collection_id(cli.collection_id)
        return

    if cli.freelech:
        torrent_info.view_by_freeleech(cli.freelech)
        return

    if cli.season:
        torrent_info.view_by_season(cli.season)
        return

    if cli.episode:
        torrent_info.view_by_episode(cli.episode)
        return

    if cli.mediainfo:
        torrent_info.view_by_mediainfo(cli.mediainfo)
        return

    if cli.alive:
        torrent_info.view_alive()
        return

    if cli.dead:
        torrent_info.view_dead()
        return

    if cli.dying:
        torrent_info.view_dying()
        return

    if cli.doubleup:
        torrent_info.view_doubleup()
        return

    if cli.featured:
        torrent_info.view_featured()
        return

    if cli.refundable:
        torrent_info.view_refundable()
        return

    if cli.stream:
        torrent_info.view_stream()
        return

    if cli.standard:
        torrent_info.view_sd()
        return

    if cli.highspeed:
        torrent_info.view_highspeed()
        return

    if cli.intern_r:
        torrent_info.view_internal()
        return

    if cli.prelease:
        torrent_info.view_personal()
        return

    # Handle case with no arguments
    if not cli:
        custom_console.print("Syntax error! Please check your commands")
        return


if __name__ == "__main__":
    main()
