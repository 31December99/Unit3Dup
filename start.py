# -*- coding: utf-8 -*-

from rich.console import Console
from common.custom_console import custom_console
from common.command import CommandLine
from common.clients.qbitt import Qbitt
from common.config import config
from unit3dup.bot import Bot
from unit3dup import pvtTracker
from unit3dup.torrent import View


console = Console(log_path=False)


def main():
    """
    Main function to handle the command line interface (CLI)
    """
    # /// Display welcome message
    custom_console.welcome_message()

    # /// Initialize command line interface
    cli = CommandLine()

    # /// Test the Tracker (always)
    tracker = pvtTracker.Unit3d(
        base_url=config.ITT_URL, api_token=config.ITT_APIKEY, pass_key=""
    )
    if tracker.get_alive(alive=True, perPage=1):
        custom_console.bot_log(f"[TRACKER HOST].... Online")

    # /// Test the torrent client
    if cli.args.scan or cli.args.upload:
        test_client_torrent = Qbitt.is_online()
        if not test_client_torrent:
            exit(1)

    # \\\ Commands options  \\\
    # Manual upload mode
    if cli.args.upload:
        unit3dup = Bot(
            path=cli.args.upload, tracker_name=cli.args.tracker, cli=cli.args
        )
        unit3dup.run()

    # Manual folder mode
    if cli.args.folder:
        unit3dup = Bot(
            path=cli.args.folder,
            tracker_name=cli.args.tracker,
            cli=cli.args,
            mode="folder",
        )
        unit3dup.run()

    # Auto mode
    if cli.args.scan and not cli.args.ftp:
        unit3dup = Bot(
            path=cli.args.scan, tracker_name=cli.args.tracker, cli=cli.args, mode="auto"
        )
        unit3dup.run()

    # Pw
    if cli.args.pw:
        unit3dup = Bot(
            path=cli.args.pw,
            tracker_name=cli.args.tracker,
            cli=cli.args,
        )
        unit3dup.pw()

    # ftp and upload
    if cli.args.ftp:
        unit3dup = Bot(
            path=cli.args.scan, tracker_name=cli.args.tracker, cli=cli.args, mode="auto"
        )
        unit3dup.ftp()
        if cli.args.scan:
            unit3dup.run()

    # Commands list: commands not necessary for upload but may be useful
    torrent_info = View()

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
        console.print("Syntax error! Please check your commands")
        return


if __name__ == "__main__":
    main()
    print()
