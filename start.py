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
    parser.add_argument("-u", "--upload", nargs=1, type=str, help="Upload Path")
    parser.add_argument("-t", "--tracker", nargs=1, type=str, help="Tracker Name")
    parser.add_argument("-s", "--search", nargs=1, type=str, help="Search")
    parser.add_argument("-i", "--info", nargs=1, type=str, help="Info")
    parser.add_argument("-up", "--uploader", nargs=1, type=str, help="Uploader user")

    parser.add_argument("-d", "--dead", action='store_true', help="Dead torrent")
    parser.add_argument("-dy", "--dying", action='store_true', help="Dying torrent")

    args = parser.parse_args()

    if args.upload:
        if not os.path.exists(args.upload[0]):
            console.log(f"Il percorso {args.upload[0]} non esiste.")
            sys.exit()

    tracker = "itt" if not args.tracker else args.tracker[0]

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

    if args.dead:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_dead()
        return

    if args.dying:
        torrent_info = Torrent(args.tracker)
        torrent_info.get_dying()
        return

    console.print("Sintassi non valida o valore nullo. Controlla..")
    console.print(f"[-u] {args.upload}")
    console.print(f"[-t] {args.tracker}")
    console.print(f"[-s] {args.search}")
    console.print(f"[-i] {args.info}")
    console.print(f"[-d] {args.dead}")
    console.print(f"[-dy] {args.dying}")


if __name__ == "__main__":
    main()
    print()

