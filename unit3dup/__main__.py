# -*- coding: utf-8 -*-

from common.torrent_clients import TransmissionClient, QbittorrentClient, RTorrentClient
from common.command import CommandLine
from common.settings import Load,DEFAULT_JSON_PATH

from unit3dup.torrent import View
from unit3dup import pvtTracker
from unit3dup.bot import Bot
from common.trackers.trackers import TRACKData

from view import custom_console

def main():
    """
    Main function to handle the command line interface (CLI)
    """

    custom_console.welcome_message()
    custom_console.bot_question_log(f"Checking your configuration file.. \n")

    # Load user configuration data
    config = Load().load_config()
    custom_console.bot_log(f"[Configuration] '{DEFAULT_JSON_PATH}'")
    custom_console.bot_log(f"[*.torrent Archive] '{config.user_preferences.TORRENT_ARCHIVE_PATH}'")
    custom_console.bot_log(f"[Images,Tmdb cache] '{config.user_preferences.CACHE_PATH}'")
    custom_console.bot_log(f"[Watcher] '{config.user_preferences.WATCHER_PATH}'")
    custom_console.bot_log(f"[Watcher] '{config.user_preferences.WATCHER_DESTINATION_PATH}'")
    print()

    # /// Initialize command line interface
    cli = CommandLine()

    # Get the torrent archive path
    if config.user_preferences.TORRENT_ARCHIVE_PATH:
        tracker_archive = config.user_preferences.TORRENT_ARCHIVE_PATH
    else:
        tracker_archive = '.'

    # /// Load the list of the registered trackers
    if not config.tracker_config.MULTI_TRACKER:
        custom_console.bot_error_log(f"No tracker name provided. Please update your configuration file")
        exit(1)


    # /// Test the Trackers
    for tracker_data in config.tracker_config.MULTI_TRACKER:
        tracker = pvtTracker.Unit3d(tracker_name=tracker_data)
        if tracker.filter_by(alive=True, perPage=10):
            custom_console.bot_log(f"Tracker -> '{tracker_data.upper()}' Online")
        else:
            if cli.args.tracker == tracker_data:
                custom_console.bot_error_log(f"Your default tracker '{tracker_data}' is offline")
                exit()


    # Test both clients only if used
    if cli.args.noseed is False and cli.args.noup is False or cli.args.reseed is True:
        # /// Test the torrent clients
        if cli.args.scan or cli.args.upload or cli.args.folder or cli.args.watcher:

            if config.torrent_client_config.TORRENT_CLIENT.lower()=="qbittorrent":
                test_client_torrent = QbittorrentClient()
                if not test_client_torrent.connect():
                    exit(1)
            elif config.torrent_client_config.TORRENT_CLIENT.lower()=="transmission":
                test_client_torrent = TransmissionClient()
                if not test_client_torrent.connect():
                    exit(1)

            elif config.torrent_client_config.TORRENT_CLIENT.lower()=="rtorrent":
                test_client_torrent = RTorrentClient()
                if not test_client_torrent.connect():
                    exit(1)

            else:
                custom_console.bot_error_log(f"Unknown Torrent Client name '{config.torrent_client_config.TORRENT_CLIENT}'")
                custom_console.bot_error_log(f"You need to set a favorite 'torrent_client' in the config file")
                exit(1)


    # Check if the tracker name exists
    if cli.args.tracker and cli.args.tracker not in config.tracker_config.MULTI_TRACKER:
       custom_console.bot_error_log(f"Tracker '{cli.args.tracker}' not found. Please update your configuration file")
       exit()

    # Get default tracker
    tracker_name_list = [config.tracker_config.MULTI_TRACKER[0]]

    # Add a single announce if requested (disabled)
    if cli.args.tracker:
        tracker_name_list = [cli.args.tracker.upper()]

    # Send content to the multi_tracker list
    if cli.args.mt:
        tracker_name_list = config.tracker_config.MULTI_TRACKER

    # Manual upload mode
    if cli.args.upload:
        bot = Bot(path=cli.args.upload, cli=cli.args, trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive)
        bot.run()

    # Manual folder mode
    if cli.args.folder:
        bot = Bot(
            path=cli.args.folder,
            cli=cli.args,
            mode="folder",
            trackers_name_list=tracker_name_list,
            torrent_archive_path=tracker_archive,
        )
        bot.run()

    # Auto mode
    if cli.args.scan and not cli.args.ftp:
        bot = Bot(path=cli.args.scan, cli=cli.args, mode="auto", trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive)
        bot.run()

    # Watcher
    if cli.args.watcher:
        bot = Bot(path=cli.args.watcher, cli=cli.args, mode="auto", trackers_name_list=tracker_name_list,
                  torrent_archive_path=tracker_archive)

        bot.watcher(duration=config.user_preferences.WATCHER_INTERVAL, watcher_path=config.user_preferences.WATCHER_PATH,
                    destination_path = config.user_preferences.WATCHER_DESTINATION_PATH)

    # Pw
    if cli.args.pw:
        bot = Bot(path=cli.args.pw,cli=cli.args, trackers_name_list=tracker_name_list)
        bot.pw()


    # ftp and upload
    if cli.args.ftp:
        bot = Bot(path='', cli=cli.args, mode="folder", trackers_name_list=tracker_name_list)
        bot.ftp()


    # Commands list: commands not necessary for upload but may be useful
    if not cli.args.tracker:
        return

    tracker_data = TRACKData.load_from_module(tracker_name=cli.args.tracker)
    torrent_info = View(tracker_name=cli.args.tracker)

    # SEARCH
    if cli.args.search:
        results = torrent_info.tracker.filter_by(search=cli.args.search)
        custom_console.bot_log(f"Filter by '{cli.args.search.upper()}'")
        torrent_info.page_view(tracker_data=results, tracker=cli.args.tracker)


    if cli.args.tmdb_id and cli.args.resolution:
        results = torrent_info.tracker.filter_by(tmdbId=cli.args.tmdb_id, resolution_id=[str(tracker_data.resolution.get(cli.args.resolution))])
        custom_console.bot_log(f"Filter by '{cli.args.tmdb_id} and  {cli.args.resolution}'")
        torrent_info.page_view(tracker_data=results, tracker=cli.args.tracker)



    # Handle case with no arguments
    if not cli.args:
        custom_console.print("Syntax error! Please check your commands")
        return

if __name__ == "__main__":
    main()
