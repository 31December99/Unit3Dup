# -*- coding: utf-8 -*-

import os
from rich.console import Console
from unit3dup.command import cli
from unit3dup.files import Files
from unit3dup.automode import Auto
from unit3dup.uploader import UploadBot
from unit3dup.search import TvShow
from unit3dup import Torrent
from unit3dup import pvtVideo, pvtTorrent

console = Console(log_path=False)


def main():

    """ Read Command line arguments """
    #cli = CommandLine()

    """ Test and load configuration files """
    # config_tracker = cli.config_load(tracker_env_name=cli.args.tracker)

    """ Auto Mode """
    if cli.args.scan:
        # New instance with cli.path
        auto = Auto(cli.args.scan)

        # Walk through the path
        series, movies = auto.scan()
        # Map the tv database

        # For each item
        for item in series:
            """
            Getting ready for tracker upload
            Return
                  - torrent name (filename or folder name)
                  - tracker name ( TODO: load config at start)
                  - content category ( movie or serie)
                  - torrent meta_info 
            """
            video_files = Files(path=item.torrent_path, tracker=cli.args.tracker)
            content = video_files.get_data()

            """ Request results from the TVshow online database """
            my_tmdb = TvShow(content.category)
            tv_show_result = my_tmdb.start(content.file_name)

            """ Return info about HD or Standard , MediaInfo, Description (screenshots), Size value for free_lech """
            video = pvtVideo.Video(
                fileName=str(os.path.join(content.folder, content.file_name))
            )

            """ Hashing """
            my_torrent = pvtTorrent.Mytorrent(contents=content, meta=content.metainfo)
            my_torrent.write()

            """ the bot is getting ready to send the payload """
            unit3d_up = UploadBot(content)
            payload = unit3d_up.payload(tv_show=tv_show_result, video=video)

            """ Send """
            # unit3d_up.send(data=payload, torrent=my_torrent)

    """ COMMANDS LIST: commands not necessary for the upload but may be useful """

    torrent_info = Torrent(cli.args.tracker)

    if cli.args.search:
        torrent_info.search(cli.args.search)
        return

    if cli.args.info:
        torrent_info.search(cli.args.info, info=True)
        return

    if cli.args.description:
        torrent_info.get_by_description(cli.args.description)
        return

    if cli.args.bdinfo:
        torrent_info.get_by_bdinfo(cli.args.bdinfo)
        return

    if cli.args.uploader:
        torrent_info.get_by_uploader(cli.args.uploader)
        return

    if cli.args.startyear:
        torrent_info.get_by_start_year(cli.args.startyear)
        return

    if cli.args.endyear:
        torrent_info.get_by_end_year(cli.args.endyear)
        return

    if cli.args.type:
        torrent_info.get_by_types(cli.args.type)
        return

    if cli.args.resolution:
        torrent_info.get_by_res(cli.args.resolution)
        return

    if cli.args.filename:
        torrent_info.get_by_filename(cli.args.filename)
        return

    if cli.args.tmdb_id:
        torrent_info.get_by_tmdb_id(cli.args.tmdb_id)
        return

    if cli.args.imdb_id:
        torrent_info.get_by_imdb_id(cli.args.imdb_id)
        return

    if cli.args.tvdb_id:
        torrent_info.get_by_tvdb_id(cli.args.tvdb_id)
        return

    if cli.args.mal_id:
        torrent_info.get_by_mal_id(cli.args.mal_id)
        return

    if cli.args.playlist_id:
        torrent_info.get_by_playlist_id(cli.args.playlist_id)
        return

    if cli.args.collection_id:
        torrent_info.get_by_collection_id(cli.args.collection_id)
        return

    if cli.args.freelech:
        torrent_info.get_by_freeleech(cli.args.freelech)
        return

    if cli.args.season:
        torrent_info.get_by_season(cli.args.season)
        return

    if cli.args.episode:
        torrent_info.get_by_episode(cli.args.episode)
        return

    if cli.args.mediainfo:
        torrent_info.get_by_mediainfo(cli.args.mediainfo)
        return

    if cli.args.alive:
        torrent_info.get_alive()
        return

    if cli.args.dead:
        torrent_info.get_dead()
        return

    if cli.args.dying:
        torrent_info.get_dying()
        return

    if cli.args.doubleup:
        torrent_info.get_doubleup()
        return

    if cli.args.featured:
        torrent_info.get_featured()
        return

    if cli.args.refundable:
        torrent_info.get_refundable()
        return

    if cli.args.stream:
        torrent_info.get_stream()
        return

    if cli.args.standard:
        torrent_info.get_sd()
        return

    if cli.args.highspeed:
        torrent_info.get_highspeed()
        return

    if cli.args.internal:
        torrent_info.get_internal()
        return

    if cli.args.personal:
        torrent_info.get_personal()
        return

    if not cli.args.check:
        console.print("Syntax error! Please check your commands")
        return


if __name__ == "__main__":
    main()
    print()
