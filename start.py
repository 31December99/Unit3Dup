# -*- coding: utf-8 -*-
import argparse
import os
import sys
from rich.console import Console

from unit3dup.uploader import UploadBot
from unit3dup.contents import Cli
from unit3dup import Torrent
from unit3dup.config import ConfigUnit3D

console = Console(log_path=False)


def config_load():
    try:
        config_unit3d = ConfigUnit3D.validate(
            tracker_env_name="itt.env", service_env_name="service.env"
        )
    except FileNotFoundError as message:
        console.log(message)


def welcome_message(message: str):
    if message:
        console.rule(f"\n\n[bold blue] Unit3D Uploader - {message.upper()}", style="#ea00d9")


def user_arguments():
    parser = argparse.ArgumentParser(description="Commands", add_help=False)

    # Config files
    parser.add_argument("-check", "--check",  action='store_true', help="Config check")

    # Upload commands
    parser.add_argument("-u", "--upload", type=str, help="Upload Path")
    parser.add_argument("-t", "--tracker", type=str, default='itt', help="Tracker Name")
    parser.add_argument("-scan", "--scan", type=str, help="Scan Folder")

    # Tracker search commands
    parser.add_argument("-s", "--search", type=str, help="Search")
    parser.add_argument("-i", "--info", type=str, help="Info")
    parser.add_argument("-up", "--uploader", type=str, help="Uploader User")
    parser.add_argument("-desc", "--description", type=str, help="Description")
    parser.add_argument("-bdinfo", "--bdinfo", type=str, help="BDInfo")
    parser.add_argument("-m", "--mediainfo", type=str, help="MediaInfo")
    parser.add_argument("-st", "--startyear", type=str, help="Start Year")
    parser.add_argument("-en", "--endyear", type=str, help="End Year")
    parser.add_argument("-type", "--type", type=str, help="Type ID")
    parser.add_argument("-res", "--resolution", type=str, help="Resolution ID")
    parser.add_argument("-file", "--filename", type=str, help="File Name")

    parser.add_argument("-se", "--season", type=str, help="Season Number")
    parser.add_argument("-ep", "--episode", type=str, help="Episode Number")
    parser.add_argument("-tmdb", "--tmdb_id", type=str, help="TMDB ID")
    parser.add_argument("-imdb", "--imdb_id", type=str, help="IMDB ID")
    parser.add_argument("-tvdb", "--tvdb_id", type=int, help="TVDB ID")
    parser.add_argument("-mal", "--mal_id", type=str, help="MAL ID")

    parser.add_argument("-playid", "--playlist_id", type=str, help="Playlist ID")
    parser.add_argument("-coll", "--collection_id", type=str, help="Collection ID")
    parser.add_argument("-free", "--freelech", type=str, help="Freelech Discount")

    parser.add_argument("-a", "--alive", action='store_true', help="Alive Torrent")
    parser.add_argument("-d", "--dead", action='store_true', help="Dead Torrent")
    parser.add_argument("-dy", "--dying", action='store_true', help="Dying Torrent")

    parser.add_argument("-du", "--doubleup", action='store_true', help="DoubleUp Torrent")
    parser.add_argument("-fe", "--featured", action='store_true', help="Featured Torrent")
    parser.add_argument("-re", "--refundable", action='store_true', help="Refundable Torrent")
    parser.add_argument("-str", "--stream", action='store_true', help="Stream Torrent")
    parser.add_argument("-sd", "--standard", action='store_true', help="Standard Definition Torrent")
    parser.add_argument("-hs", "--highspeed", action='store_true', help="Highspeed Torrent")
    parser.add_argument("-int", "--internal", action='store_true', help="Internal Torrent")
    parser.add_argument("-pers", "--personal", action='store_true', help="Personal Release Torrent")

    args = parser.parse_args()
    tracker = args.tracker

    if args.upload and not os.path.exists(args.upload):
        console.log(f"The path {args.upload} does not exist.")
        sys.exit()

    if not os.path.exists(f"{tracker}.env"):
        console.log(f"Configuration file '{tracker}.env' not found for tracker '{tracker}'")
        sys.exit()

    if not os.path.exists(f"{tracker}.json"):
        console.log(f"Configuration file '{tracker}.json' not found for tracker '{tracker}'")
        sys.exit()

    return args


def start_info(bot):
    console.log(f"\n[TORRENT NAME] {bot.name}")


def process_upload(user_content):
    bot = UploadBot(user_content)
    start_info(bot)
    data = bot.serie_data() if user_content.category == 2 else bot.movie_data()
    bot.process_data(data)


def main():
    """
    Command line
    """
    args = user_arguments()


    """
    Load the configuration and perform a few checks
    """
    if args.check:
        config_load()

    """
    UPLOAD: manual upload for series and movies
    A folder path represents a series
    A file path represents a movie
    """

    if args.upload:
        # Get file path
        path = Cli(path=args.upload, tracker=args.tracker)
        if path:
            # Preparing a movie/serie for upload
            data = path.get_data()
            welcome_message(args.upload)
            # Upload to tracker
            process_upload(data) if data else None
            return

    """
    AUTO UPLOAD: scans the path
    All files in the path are considered movies if they do not have SxEx tags
    Each subfolder represents a series TODO: series not yet implemented
    """

    if args.scan:
        # Set Main path
        path = Cli(path=args.scan, tracker=args.tracker)
        # Return File object movies and series
        movies, series = path.scan()
        # Each file gets metadata, uploaded, and seeded

        for movie in movies:
            if movie:
                welcome_message(movie.file_name)
                # Get file path
                path = Cli(path=movie.file_name, tracker=args.tracker)
                if path:
                    # Preparing a movie for upload
                    data = path.get_data()
                    # Upload to tracker
                    process_upload(data) if data else None

        # Same as with movies
        for serie in series:
            if serie:
                welcome_message(serie.folder)
                # Get file path
                path = Cli(path=serie.folder, tracker=args.tracker)
                if path:
                    # Preparing a movie for upload
                    data = path.get_data()
                    # Upload to tracker
                    process_upload(data) if data else None
        return

    """
    COMMANDS LIST: commands not necessary for the upload but may be useful
    """

    torrent_info = Torrent(args.tracker)

    if args.search:
        torrent_info.search(args.search)
        return

    if args.info:
        torrent_info.search(args.info, info=True)
        return

    if args.description:
        torrent_info.get_by_description(args.description)
        return

    if args.bdinfo:
        torrent_info.get_by_bdinfo(args.bdinfo)
        return

    if args.uploader:
        torrent_info.get_by_uploader(args.uploader)
        return

    if args.startyear:
        torrent_info.get_by_start_year(args.startyear)
        return

    if args.endyear:
        torrent_info.get_by_end_year(args.endyear)
        return

    if args.type:
        torrent_info.get_by_types(args.type)
        return

    if args.resolution:
        torrent_info.get_by_res(args.resolution)
        return

    if args.filename:
        torrent_info.get_by_filename(args.filename)
        return

    if args.tmdb_id:
        torrent_info.get_by_tmdb_id(args.tmdb_id)
        return

    if args.imdb_id:
        torrent_info.get_by_imdb_id(args.imdb_id)
        return

    if args.tvdb_id:
        torrent_info.get_by_tvdb_id(args.tvdb_id)
        return

    if args.mal_id:
        torrent_info.get_by_mal_id(args.mal_id)
        return

    if args.playlist_id:
        torrent_info.get_by_playlist_id(args.playlist_id)
        return

    if args.collection_id:
        torrent_info.get_by_collection_id(args.collection_id)
        return

    if args.freelech:
        torrent_info.get_by_freeleech(args.freelech)
        return

    if args.season:
        torrent_info.get_by_season(args.season)
        return

    if args.episode:
        torrent_info.get_by_episode(args.episode)
        return

    if args.mediainfo:
        torrent_info.get_by_mediainfo(args.mediainfo)
        return

    if args.alive:
        torrent_info.get_alive()
        return

    if args.dead:
        torrent_info.get_dead()
        return

    if args.dying:
        torrent_info.get_dying()
        return

    if args.doubleup:
        torrent_info.get_doubleup()
        return

    if args.featured:
        torrent_info.get_featured()
        return

    if args.refundable:
        torrent_info.get_refundable()
        return

    if args.stream:
        torrent_info.get_stream()
        return

    if args.standard:
        torrent_info.get_sd()
        return

    if args.highspeed:
        torrent_info.get_highspeed()
        return

    if args.internal:
        torrent_info.get_internal()
        return

    if args.personal:
        torrent_info.get_personal()
        return

    if not args.check:
        console.print("Syntax error! Please check your commands")


if __name__ == "__main__":
    main()
    print()
