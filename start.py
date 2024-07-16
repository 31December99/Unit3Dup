# -*- coding: utf-8 -*-
import argparse
import os
import sys

from unit3dup.uploader import UploadBot
from unit3dup.contents import Cli
from rich.console import Console
from unit3dup import Torrent

console = Console(log_path=False)


def user_arguments():
    parser = argparse.ArgumentParser(description="Commands", add_help=False)

    # // Upload commands
    parser.add_argument("-u", "--upload", nargs=1, type=str, help="Upload Path")
    parser.add_argument("-t", "--tracker", nargs=1, type=str, default=['itt'], help="Tracker Name")

    # // Tracker search commands
    parser.add_argument("-s", "--search", nargs=1, type=str, help="Search")
    parser.add_argument("-i", "--info", nargs=1, type=str, help="Info")
    parser.add_argument("-up", "--uploader", nargs=1, type=str, help="Uploader user")
    parser.add_argument("-m", "--mediainfo", nargs=1, type=str, help="Mediainfo")
    parser.add_argument("-st", "--startyear", nargs=1, type=str, help="Start Year")
    parser.add_argument("-en", "--endyear", nargs=1, type=str, help="End Year")
    parser.add_argument("-type", "--type", nargs=1, type=str, help="Type ID")
    parser.add_argument("-res", "--resolution", nargs=1, type=str, help="Resolution ID")
    parser.add_argument("-file", "--filename", nargs=1, type=str, help="File name")

    parser.add_argument("-tmdb", "--tmdb_id", nargs=1, type=str, help="TMDB ID")
    parser.add_argument("-imdb", "--imdb_id", nargs=1, type=str, help="IMDB ID")
    parser.add_argument("-tvdb", "--tvdb_id", nargs=1, type=int, help="TVDB ID")
    parser.add_argument("-mal", "--mal_id", nargs=1, type=str, help="MAL ID")

    parser.add_argument("-a", "--alive", action='store_true', help="Alive torrent")
    parser.add_argument("-d", "--dead", action='store_true', help="Dead torrent")
    parser.add_argument("-dy", "--dying", action='store_true', help="Dying torrent")

    args = parser.parse_args()
    tracker = args.tracker[0]

    if args.upload:
        if not os.path.exists(args.upload[0]):
            console.log(f"Il percorso {args.upload[0]} non esiste.")
            sys.exit()

    if not os.path.exists(f"{tracker}.env"):
        console.log(
            f"Non trovo il file di configurazione '{tracker}.env' per il tracker '{tracker}'"
        )
        sys.exit()

    if not os.path.exists(f"{tracker}.json"):
        console.log(
            f"Non trovo il file di configurazione '{tracker}.json' per il tracker '{tracker}'"
        )
        sys.exit()
    return args


def start_info(bot, user_input):
    console.log(f"\n[TORRENT NAME] {bot.name}")
    console.log(f"[SIZE]         {user_input.size}")


def process_upload(user_input):
    bot = UploadBot(user_input.content)
    start_info(bot, user_input)
    if user_input.content.category == user_input.serie:
        data = bot.serie_data()
    else:
        data = bot.movie_data()
    bot.process_data(data)


def main():
    args = user_arguments()

    console.rule(f"\n[bold blue] Unit3D uploader", style="#ea00d9")
    if args.upload:
        user_input = Cli(args=args, tracker=args.tracker)
        if user_input:
            process_upload(user_input)
            return

    if args.search:
        torrent_info = Torrent(args.tracker)
        torrent_info.search(args.search)
        return

    if args.info:
        torrent_info = Torrent(args.tracker)
        torrent_info.search(args.info, info=True)
        return

    if args.uploader:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_uploader(args.uploader)
        return

    if args.startyear:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_start_year(args.startyear)
        return

    if args.endyear:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_end_year(args.endyear)
        return

    if args.type:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_types(args.type)
        return

    if args.resolution:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_res(args.resolution)
        return

    if args.filename:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_filename(args.filename)
        return

    if args.tmdb_id:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_tmdb_id(args.tmdb_id[0])
        return

    if args.imdb_id:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_imdb_id(args.imdb_id[0])
        return

    if args.tvdb_id:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_tvdb_id(args.tvdb_id[0])
        return

    if args.mal_id:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_mal_id(args.mal_id[0])
        return

    if args.mediainfo:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_by_mediainfo(args.mediainfo)
        return

    if args.alive:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_alive()
        return

    if args.dead:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_dead()
        return

    if args.dying:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_dying()
        return

    console.print("Sintassi non valida o valore nullo. Controlla..")


if __name__ == "__main__":
    main()
    print()
