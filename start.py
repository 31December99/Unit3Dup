# -*- coding: utf-8 -*-

from rich.console import Console
from unit3dup.torrent import View
from unit3dup.command import CommandLine
from unit3dup import config
from unit3dup.ping import Ping
from unit3dup.media import Media

console = Console(log_path=False)


def main():
    """Manual Mode"""
    if cli.args.upload:
        media_video = Media(path=cli.args.upload, tracker_name=cli.args.tracker)
        media_video.process()

    """ Auto Mode """
    if cli.args.scan:
        media_video = Media(path=cli.args.scan, tracker_name=cli.args.tracker)
        media_video.process(mode="auto")

    """ COMMANDS LIST: commands not necessary for the upload but may be useful """

    torrent_info = View()

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

    if not cli.args:
        console.print("Syntax error! Please check your commands")
        return


if __name__ == "__main__":

    cli = CommandLine()
    config = config.trackers.get_tracker("itt")

    """ Test configuration"""
    ping = Ping()
    console.rule("\nChecking configuration files")
    # always ping the tracker
    track_err = ping.process_tracker()
    # Ping only if scanning is selected
    if cli.args.scan or cli.args.upload:
        qbit_err = ping.process_qbit()
        tmdb_err = ping.process_tmdb()
        imghost_err = ping.process_imghost()
        if not (tmdb_err and qbit_err and imghost_err and track_err):
            console.log("Check your configuration file. Exit..")
            exit(1)

    main()
    print()
