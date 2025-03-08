# -*- coding: utf-8 -*-

from common.torrent_clients import TransmissionClient, QbittorrentClient
from common.command import CommandLine
from common.settings import Load

from unit3dup.torrent import View
from unit3dup import pvtTracker
from unit3dup.bot import Bot

from view import custom_console

def main():
    """
    Main function to handle the command line interface (CLI)
    """

    custom_console.welcome_message()
    custom_console.bot_question_log(f"Checking your configuration file.. \n")

    # Load user configuration data
    config = Load().load_config()

    # /// Initialize command line interface
    cli = CommandLine()

    # /// Load the list of the registered trackers
    if not config.tracker_config.MULTI_TRACKER:
        custom_console.bot_error_log(f"No tracker name provided. Please update your configuration file")
        exit(1)

    # /// Test the Tracker
    for tracker_data in config.tracker_config.MULTI_TRACKER:
        tracker = pvtTracker.Unit3d(tracker=tracker_data)
        if tracker.get_alive(alive=True, perPage=1):
            custom_console.bot_log(f"Tracker -> '{tracker_data.upper()}' Online")
            pass


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
        else:
            custom_console.bot_error_log(f"Unknown Torrent Client name '{config.torrent_client_config.TORRENT_CLIENT}'")
            custom_console.bot_error_log(f"You need to set a favorite 'torrent_client' in the config file")
            exit(1)


    # \\\ Commands options  \\\
    force_media = None # todo

    # Manual upload mode
    if cli.args.upload:
        bot = Bot(path=cli.args.upload, cli=cli.args)
        bot.run()

    # Manual folder mode
    if cli.args.folder:
        bot = Bot(
            path=cli.args.folder,
            cli=cli.args,
            mode="folder",
        )
        bot.run()

    # Auto mode
    if cli.args.scan and not cli.args.ftp:
        bot = Bot(path=cli.args.scan, cli=cli.args, mode="auto")
        bot.run()

    # Watcher
    if cli.args.watcher:
        bot = Bot(path=cli.args.watcher, cli=cli.args, mode="auto")

        bot.watcher(duration=config.user_preferences.WATCHER_INTERVAL, watcher_path=config.user_preferences.WATCHER_PATH,
                    destination_path = config.user_preferences.WATCHER_DESTINATION_PATH)


    # Pw
    if cli.args.pw:
        bot = Bot(path=cli.args.pw,cli=cli.args)
        bot.pw()


    # ftp and upload
    if cli.args.ftp:
        bot = Bot(path='', cli=cli.args, mode="folder")
        bot.ftp()


    # Commands list: commands not necessary for upload but may be useful
    if not cli.args.tracker:
        return

    torrent_info = View(tracker_name=cli.args.tracker)

    # Search by different criteria
    if cli.args.search:
        torrent_info.view_search(cli.args.search)
        return

    if cli.args.info:
        torrent_info.view_search(cli.args.info, info=True)
        return

    if cli.args.description:
        torrent_info.view_by_description(cli.args.description)
        return

    if cli.args.bdinfo:
        torrent_info.view_by_bdinfo(cli.args.bdinfo)
        return

    if cli.args.uploader:
        torrent_info.view_by_uploader(cli.args.uploader)
        return

    if cli.args.startyear:
        torrent_info.view_by_start_year(cli.args.startyear)
        return

    if cli.args.endyear:
        torrent_info.view_by_end_year(cli.args.endyear)
        return

    if cli.args.type:
        torrent_info.view_by_types(cli.args.type)
        return

    if cli.args.resolution:
        torrent_info.view_by_res(cli.args.resolution)
        return

    if cli.args.filename:
        torrent_info.view_by_filename(cli.args.filename)
        return

    if cli.args.tmdb_id:
        torrent_info.view_by_tmdb_id(cli.args.tmdb_id)
        return

    if cli.args.imdb_id:
        torrent_info.view_by_imdb_id(cli.args.imdb_id)
        return

    if cli.args.tvdb_id:
        torrent_info.view_by_tvdb_id(cli.args.tvdb_id)
        return

    if cli.args.mal_id:
        torrent_info.view_by_mal_id(cli.args.mal_id)
        return

    if cli.args.playlist_id:
        torrent_info.view_by_playlist_id(cli.args.playlist_id)
        return

    if cli.args.collection_id:
        torrent_info.view_by_collection_id(cli.args.collection_id)
        return

    if cli.args.freelech:
        torrent_info.view_by_freeleech(cli.args.freelech)
        return

    if cli.args.season:
        torrent_info.view_by_season(cli.args.season)
        return

    if cli.args.episode:
        torrent_info.view_by_episode(cli.args.episode)
        return

    if cli.args.mediainfo:
        torrent_info.view_by_mediainfo(cli.args.mediainfo)
        return

    if cli.args.alive:
        torrent_info.view_alive()
        return

    if cli.args.dead:
        torrent_info.view_dead()
        return

    if cli.args.dying:
        torrent_info.view_dying()
        return

    if cli.args.doubleup:
        torrent_info.view_doubleup()
        return

    if cli.args.featured:
        torrent_info.view_featured()
        return

    if cli.args.refundable:
        torrent_info.view_refundable()
        return

    if cli.args.stream:
        torrent_info.view_stream()
        return

    if cli.args.standard:
        torrent_info.view_sd()
        return

    if cli.args.highspeed:
        torrent_info.view_highspeed()
        return

    if cli.args.internal:
        torrent_info.view_internal()
        return

    if cli.args.personal:
        torrent_info.view_personal()
        return

    # Handle case with no arguments
    if not cli.args:
        custom_console.print("Syntax error! Please check your commands")
        return

if __name__ == "__main__":
    main()
    print()
