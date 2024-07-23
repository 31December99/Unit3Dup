# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
from rich.console import Console

from unit3dup.uploader import UploadBot
from unit3dup.contents import Cli
from unit3dup import Torrent
from unit3dup.config import ConfigUnit3D
from unit3dup import userinput, title

from Unit3Dup_2.MediaFiles import Files, Folders

console = Console(log_path=True)


def config_load():
    try:
        config_unit3d = ConfigUnit3D.validate(
            tracker_env_name="itt.env", service_env_name="service.env"
        )
    except FileNotFoundError as message:
        console.log(message)


def welcome_message(message: str):
    if message:
        console.rule(f"[bold blue]{message.upper()}", style="#ea00d9")


def user_arguments():
    parser = argparse.ArgumentParser(description="Commands", add_help=False)

    # Config files
    parser.add_argument("-check", "--check", action='store_true', help="Config check")

    # Upload commands
    parser.add_argument("-u", "--upload", type=str, help="Upload Path")
    parser.add_argument("-t", "--tracker", type=str, default='itt', help="Tracker Name")
    parser.add_argument("-scan", "--scan", type=str, help="Scan Folder")

    # Tracker search commands
    parser.add_argument("-s", "--search", type=str, help="Search")

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
    console.log(f"\n[TORRENT NAME]......... {bot.name}")


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

    is_dir = os.path.isdir(args.scan) if args.scan else None
    print(is_dir)

    if is_dir is False:
        welcome_message(args.tracker)
        path_files = Files(path=args.scan, tracker=args.tracker)
        data = path_files.get_data()
        print(vars(data))

    if is_dir is True:
        welcome_message(args.tracker)
        path_folders = Folders(path=args.scan, tracker=args.tracker)
        data = path_folders.get_data()

        print(data)


    path = Cli(path=args.scan, tracker=args.tracker)

    if not path.is_dir:
        # Check for valid extension
        process = path.process_file() if path.filter_ext(path.path) else False
        print("File", process)

    else:
        process = path.process_folder()
        print("Folder", process)


if __name__ == "__main__":
    main()
    print()
