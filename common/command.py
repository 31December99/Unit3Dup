# -*- coding: utf-8 -*-
import os
import argparse

from common.utility import System
from common.settings import Load


class CommandLine:
    """
    Handle command line arguments
    """

    def __init__(self):

        # Load config
        config = Load().load_config()

        # /////////////////////////
        # Main parser
        # /////////////////////////
        parser = argparse.ArgumentParser(
            description="Manage torrents, uploads, searches and config checks",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # /////////////////////////
        # Groups
        # /////////////////////////
        cfg_group = parser.add_argument_group("Config Commands")
        upload_group = parser.add_argument_group("Upload Commands")
        search_group = parser.add_argument_group("Search Commands")
        filter_group = parser.add_argument_group("Filter Options")
        special_group = parser.add_argument_group("Special Flags")

        # /////////////////////////
        # Config Commands
        # /////////////////////////
        cfg_group.add_argument(
            "-check", "--check",
            action="store_true",
            help="Check config files"
        )

        # /////////////////////////
        # Upload Commands
        # /////////////////////////
        upload_group.add_argument("-u", "--upload", type=str, help="Upload path")
        upload_group.add_argument("-f", "--folder", type=str, help="Upload folder")
        upload_group.add_argument("-scan", "--scan", type=str, help="Scan folder")
        upload_group.add_argument("-b", "--buildtags", action="store_true", help="Auto build title")
        upload_group.add_argument("-reseed", "--reseed", action="store_true", help="Reseed folder")
        upload_group.add_argument("-watcher", "--watcher", action="store_true", help="Start watcher")
        upload_group.add_argument("-notitle", "--notitle", type=str, help="Manual title")

        upload_group.add_argument(
            "-tracker", "--tracker",
            type=str,
            default=config.tracker_config.MULTI_TRACKER[0],
            help="Single tracker"
        )

        upload_group.add_argument("-mt", "--mt", action="store_true", help="Multi tracker")

        upload_group.add_argument(
            "-force",
            nargs='?',
            const="movie",
            type=str,
            default=None,
            help="Force category"
        )

        upload_group.add_argument("-noseed", "--noseed", action="store_true", help="Disable seeding")
        upload_group.add_argument("-noup", "--noup", action="store_true", help="Torrent only")
        upload_group.add_argument("-dup", "--duplicate", action="store_true", help="Check duplicates")
        upload_group.add_argument("-personal", "--personal", action="store_true", help="Personal release")
        upload_group.add_argument("-ftp", "--ftp", action="store_true", help="Connect FTP")

        # /////////////////////////
        # Search Commands
        # /////////////////////////
        search_group.add_argument("-dmp", "--dump", action="store_true", help="Dump titles")
        search_group.add_argument("-sch", "--search", type=str, help="Search torrent")
        search_group.add_argument("-db", "--dbsave", action="store_true", help="Save results")
        search_group.add_argument("-i", "--info", type=str, help="Torrent info")
        search_group.add_argument("-up", "--uploader", type=str, help="By uploader")
        search_group.add_argument("-d", "--description", type=str, help="By description")
        search_group.add_argument("-bd", "--bdinfo", type=str, help="Show BDInfo")
        search_group.add_argument("-m", "--mediainfo", type=str, help="Show MediaInfo")

        # /////////////////////////
        # Filter Options
        # /////////////////////////
        filter_group.add_argument("-st", "--startyear", type=str, help="Start year")
        filter_group.add_argument("-en", "--endyear", type=str, help="End year")
        filter_group.add_argument("-type", "--type", type=str, help="Type")
        filter_group.add_argument("-res", "--resolution", type=str, help="Resolution")
        filter_group.add_argument("-file", "--filename", type=str, help="Filename")
        filter_group.add_argument("-se", "--season", type=str, help="Season")
        filter_group.add_argument("-ep", "--episode", type=str, help="Episode")

        # IDs
        filter_group.add_argument("-tmdb", "--tmdb_id", type=str, help="TMDB ID")
        filter_group.add_argument("-imdb", "--imdb_id", type=str, help="IMDB ID")
        filter_group.add_argument("-tvdb", "--tvdb_id", type=int, help="TVDB ID")
        filter_group.add_argument("-mal", "--mal_id", type=str, help="MAL ID")
        filter_group.add_argument("-playid", "--playlist_id", type=str, help="Playlist ID")
        filter_group.add_argument("-coll", "--collection_id", type=str, help="Collection ID")

        # Status
        filter_group.add_argument("-free", "--freelech", type=str, help="Freeleech")
        filter_group.add_argument("-al", "--alive", action="store_true", help="Alive")
        filter_group.add_argument("-dd", "--dead", action="store_true", help="Dead")
        filter_group.add_argument("-dy", "--dying", action="store_true", help="Dying")

        # /////////////////////////
        # Special Flags
        # /////////////////////////
        special_group.add_argument("-du", "--doubleup", action="store_true", help="DoubleUp")
        special_group.add_argument("-fe", "--featured", action="store_true", help="Featured")
        special_group.add_argument("-re", "--refundable", action="store_true", help="Refundable")
        special_group.add_argument("-str", "--stream", action="store_true", help="Stream")
        special_group.add_argument("-sd", "--standard", action="store_true", help="SD")
        special_group.add_argument("-hs", "--highspeed", action="store_true", help="Highspeed")
        special_group.add_argument("-int", "--internal", action="store_true", help="Internal")
        special_group.add_argument("-pr", "--prelease", action="store_true", help="Personal")

        # /////////////////////////
        # Parse args
        # /////////////////////////
        self.args = parser.parse_args()

        # /////////////////////////
        # Check scan path
        # /////////////////////////
        self.is_dir = os.path.isdir(self.args.scan) if self.args.scan else None

        # /////////////////////////
        # Expand upload path
        # /////////////////////////
        if self.args.upload:
            self.args.upload = os.path.expanduser(self.args.upload)

        # /////////////////////////
        # Validate force category
        # /////////////////////////
        if self.args.force:

            self.args.force = self.args.force[:10]

            valid_categories = [
                System.category_list[System.MOVIE],
                System.category_list[System.GAME],
                System.category_list[System.TV_SHOW],
                System.category_list[System.DOCUMENTARY]
            ]

            if self.args.force.lower() not in valid_categories:
                self.args.force = None
                print("Invalid -force category")
                exit()
