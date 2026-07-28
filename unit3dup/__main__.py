# -*- coding: utf-8 -*-

from unit3dup.external.torrent.torrent_clients import (
    TransmissionClient,
    QbittorrentClient,
    RTorrentClient,
)
from unit3dup.external.torrent.torrent import View
from unit3dup.external.tracker import pvtTracker

from unit3dup.bot.bot import Bot
from unit3dup.bot.command import CommandLine
from unit3dup.config.bot_config import BotConfig
from unit3dup.config.settings import (
    Load,
    DEFAULT_JSON_PATH,
    version,
)

from unit3dup.shared.utility import System
from unit3dup.view import custom_console


def main():
    """
    command line interface (CLI)
    """

    custom_console.welcome_message()

    custom_console.bot_question_log(
        f"Unit3Dup {version} "
        "Checking your configuration file..\n"
    )

    # Load user configuration data
    config = Load().config

    custom_console.bot_log(
        f"[Configuration] '{DEFAULT_JSON_PATH}'"
    )
    custom_console.bot_log(
        "[*.torrent Archive] "
        f"'{config.user_preferences.TORRENT_ARCHIVE_PATH}'"
    )
    custom_console.bot_log(
        "[Images,Tmdb cache] "
        f"'{config.user_preferences.CACHE_PATH}'"
    )
    custom_console.bot_log(
        f"[Watcher] '{config.user_preferences.WATCHER_PATH}'"
    )
    custom_console.bot_log(
        "[Watcher] "
        f"'{config.user_preferences.WATCHER_DESTINATION_PATH}'"
    )
    custom_console.bot_log(
        "[Preferred Language] "
        f"'{config.user_preferences.PREFERRED_LANG}'"
    )
    custom_console.bot_log(
        "[Youtube Preferred Language] "
        f"'{config.user_preferences.YOUTUBE_PREF_LANG}'"
    )

    print()

    # Initialize command line interface
    user = CommandLine()

    # Decouple user args from the CLI namespace
    cli = BotConfig.from_namespace(user.args)

    tracker_name_list = System.get_tracker_name_list(
        cli=cli,
        config=config,
    )

    # Check configured trackers
    if tracker_name_list:
        for tracker_data in tracker_name_list:
            tracker = pvtTracker.Unit3d(
                tracker_name=tracker_data,
            )

            if tracker.get_alive(
                    alive=True,
                    perPage=1,
            ):
                custom_console.bot_log(
                    f"Tracker -> "
                    f"'{tracker_data.upper()}' Online"
                )

    # Add multi-tracker list
    if cli.mt:
        tracker_name_list = (
            config.tracker_config.MULTI_TRACKER
        )

        for tracker_data in tracker_name_list[1:]:
            tracker = pvtTracker.Unit3d(
                tracker_name=tracker_data,
            )

            if tracker.get_alive(
                    alive=True,
                    perPage=1,
            ):
                custom_console.bot_log(
                    f"Tracker -> "
                    f"'{tracker_data.upper()}' Online"
                )

    # Test torrent client only if required
    if (
            cli.noseed is False
            and cli.noup is False
    ) or cli.reseed is True:

        if (
                cli.scan
                or cli.upload
                or cli.folder
                or cli.watcher
        ):
            torrent_client = (
                config.torrent_client_config
                .TORRENT_CLIENT
                .lower()
            )

            if torrent_client == "qbittorrent":
                test_client_torrent = (
                    QbittorrentClient()
                )

            elif torrent_client == "transmission":
                test_client_torrent = (
                    TransmissionClient()
                )

            elif torrent_client == "rtorrent":
                test_client_torrent = (
                    RTorrentClient()
                )

            else:
                custom_console.bot_error_log(
                    "Unknown Torrent Client name "
                    f"'{config.torrent_client_config.TORRENT_CLIENT}'"
                )

                custom_console.bot_error_log(
                    "You need to set a favorite "
                    "'torrent_client' in the config file"
                )

                exit(1)

            if not test_client_torrent.connect():
                exit(1)

    # Run
    if (
            cli.upload
            or cli.folder
            or (
            cli.scan
            and not cli.ftp
    )
    ):
        bot = Bot(
            cli=cli,
            trackers_name_list=tracker_name_list,
            torrent_archive_path=(
                config.user_preferences
                .TORRENT_ARCHIVE_PATH
            ),
        )

        bot.run()

    # Watcher
    if cli.watcher:
        bot = Bot(
            cli=cli,
            trackers_name_list=tracker_name_list,
            torrent_archive_path=(
                config.user_preferences
                .TORRENT_ARCHIVE_PATH
            ),
        )

        bot.watcher(
            duration=(
                config.user_preferences
                .WATCHER_INTERVAL
            ),
            watcher_path=(
                config.user_preferences
                .WATCHER_PATH
            ),
            destination_path=(
                config.user_preferences
                .WATCHER_DESTINATION_PATH
            ),
        )

    # FTP and upload
    if cli.ftp:
        bot = Bot(
            cli=cli,
            trackers_name_list=tracker_name_list,
            torrent_archive_path=(
                config.user_preferences
                .TORRENT_ARCHIVE_PATH
            ),
        )

        bot.ftp()

    # Tracker commands
    if not cli.tracker:
        return

    torrent_info = View(
        tracker_name=cli.tracker,
    )

    # ------------------------------------------------------------------
    # /// Combo filters
    # ------------------------------------------------------------------

    if cli.tmdb_id and cli.resolution:
        torrent_info.view_tmdb_res(
            cli.tmdb_id,
            cli.resolution,
        )
        return

    # ------------------------------------------------------------------
    # /// Search
    # ------------------------------------------------------------------

    if cli.search:
        torrent_info.view_search(
            cli.search,
            save=cli.dbsave,
        )
        return

    # Dump
    if cli.dump:
        torrent_info.view_search(
            " ",
            inkey=False,
            save=True,
        )
        return

    # Info
    if cli.info:
        torrent_info.view_search(
            cli.info,
            info=True,
        )
        return

    # ------------------------------------------------------------------
    # /// Text filters
    # ------------------------------------------------------------------

    if cli.description:
        torrent_info.view_by_description(
            cli.description,
        )
        return

    if cli.bdinfo:
        torrent_info.view_by_bdinfo(
            cli.bdinfo,
        )
        return

    if cli.uploader:
        torrent_info.view_by_uploader(
            cli.uploader,
            save=cli.dbsave,
        )
        return

    if cli.startyear:
        torrent_info.view_by_start_year(
            cli.startyear,
        )
        return

    if cli.endyear:
        torrent_info.view_by_end_year(
            cli.endyear,
        )
        return

    if cli.mediainfo:
        torrent_info.view_by_mediainfo(
            cli.mediainfo,
        )
        return

    # ------------------------------------------------------------------
    # /// Type , Resolution
    # ------------------------------------------------------------------

    if cli.type:
        torrent_info.view_by_types(
            cli.type,
        )
        return

    if cli.resolution:
        torrent_info.view_by_res(
            cli.resolution,
        )
        return

    if cli.filename:
        torrent_info.view_by_filename(
            cli.filename,
        )
        return

    # ------------------------------------------------------------------
    # /// external ID
    # ------------------------------------------------------------------

    if cli.tmdb_id:
        torrent_info.view_by_tmdb_id(
            cli.tmdb_id,
        )
        return

    if cli.imdb_id:
        torrent_info.view_by_imdb_id(
            cli.imdb_id,
        )
        return

    if cli.tvdb_id:
        torrent_info.view_by_tvdb_id(
            cli.tvdb_id,
        )
        return

    if cli.mal_id:
        torrent_info.view_by_mal_id(
            cli.mal_id,
        )
        return

    # ------------------------------------------------------------------
    # /// Playlist, Collection
    # ------------------------------------------------------------------

    if cli.playlist_id:
        torrent_info.view_by_playlist_id(
            cli.playlist_id,
        )
        return

    if cli.collection_id:
        torrent_info.view_by_collection_id(
            cli.collection_id,
        )
        return

    # ------------------------------------------------------------------
    # /// Torrent filters
    # ------------------------------------------------------------------

    if cli.freelech:
        torrent_info.view_by_freeleech(
            cli.freelech,
        )
        return

    if cli.season:
        torrent_info.view_by_season(
            cli.season,
        )
        return

    if cli.episode:
        torrent_info.view_by_episode(
            cli.episode,
        )
        return

    # ------------------------------------------------------------------
    # /// Boolean filters
    # ------------------------------------------------------------------

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

    if not cli:
        custom_console.print(
            "Syntax error! Please check your commands"
        )
        return


if __name__ == "__main__":
    main()
