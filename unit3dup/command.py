# -*- coding: utf-8 -*-
import os
from rich.console import Console

import argparse
import sys

console = Console(log_path=False)


class CommandLine:
    """
    Classe per prendere come input il percorso dell'user da riga di comando
    """

    def __init__(self):
        parser = argparse.ArgumentParser(description="Commands", add_help=False)

        # Config files
        parser.add_argument(
            "-check", "--check", action="store_true", help="Config check"
        )

        # Upload commands
        parser.add_argument("-u", "--upload", type=str, help="Upload Path")
        parser.add_argument(
            "-t", "--tracker", type=str, default="itt", help="Tracker Name"
        )
        parser.add_argument("-scan", "--scan", type=str, help="Scan Folder")

        parser.add_argument(
            "-torrent", "--torrent", action="store_true", help="Create torrent only"
        )

        parser.add_argument(
            "-duplicate",
            "--duplicate",
            action="store_true",
            help="Search for duplicate only",
        )

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

        parser.add_argument("-a", "--alive", action="store_true", help="Alive Torrent")
        parser.add_argument("-d", "--dead", action="store_true", help="Dead Torrent")
        parser.add_argument("-dy", "--dying", action="store_true", help="Dying Torrent")

        parser.add_argument(
            "-du", "--doubleup", action="store_true", help="DoubleUp Torrent"
        )
        parser.add_argument(
            "-fe", "--featured", action="store_true", help="Featured Torrent"
        )
        parser.add_argument(
            "-re", "--refundable", action="store_true", help="Refundable Torrent"
        )
        parser.add_argument(
            "-str", "--stream", action="store_true", help="Stream Torrent"
        )
        parser.add_argument(
            "-sd", "--standard", action="store_true", help="Standard Definition Torrent"
        )
        parser.add_argument(
            "-hs", "--highspeed", action="store_true", help="Highspeed Torrent"
        )
        parser.add_argument(
            "-int", "--internal", action="store_true", help="Internal Torrent"
        )
        parser.add_argument(
            "-pers", "--personal", action="store_true", help="Personal Release Torrent"
        )
        self.args: parser = parser.parse_args()
        self.is_dir = os.path.isdir(self.args.scan) if self.args.scan else None

        if self.args.upload and not os.path.exists(self.args.upload):
            console.log(f"The path {self.args.upload} does not exist.")
            sys.exit()

        if not os.path.exists(f"{self.args.tracker}.env"):
            console.log(
                f"Configuration file '{self.args.tracker}.env' not found for tracker '{self.args.tracker}'"
            )
            sys.exit()

        if not os.path.exists(f"service.env"):
            console.log(f"Configuration file 'service.env' not found")
            sys.exit()

        database_tracker = os.path.join("trackers", f"{self.args.tracker}.json")
        if not os.path.exists(database_tracker):
            console.log(
                f"Configuration file '{self.args.tracker}.json' not found for tracker '{self.args.tracker}'"
            )
            sys.exit()
