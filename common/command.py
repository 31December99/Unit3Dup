import os
import argparse
import sys

from view import custom_console

class CommandLine:
    """
    Class to handle user input from the command line
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Manage torrents, uploads, and config checks."
        )

        # Config files
        parser.add_argument(
            "-check", "--check", action="store_true", help="Check config"
        )

        # Upload commands
        parser.add_argument("-u", "--upload", type=str, help="Upload path")
        parser.add_argument("-f", "--folder", type=str, help="Upload folder")
        parser.add_argument("-scan", "--scan", type=str, help="Scan folder")
        parser.add_argument("-watcher", "--watcher", action="store_true", help="Start watcher")
        parser.add_argument("-multi", "--multi", action="store_true", help="Upload to multi tracker")

        parser.add_argument("-pw", "--pw", type=str, help="")
        parser.add_argument("-ftp", "--ftp", action="store_true", help="Connect to FTP")
        parser.add_argument("-game", "--game", action="store_true", help="Set media type to game")
        parser.add_argument("-movie", "--movie", action="store_true", help="Set media type to movie")
        parser.add_argument("-serie", "--serie", action="store_true", help="Set media type to series")


        parser.add_argument(
            "-noupload", "--noupload", action="store_true", help="Create torrent only"
        )

        parser.add_argument(
            "-duplicate",
            "--duplicate",
            action="store_true",
            help="Find duplicates"
        )

        # Tracker search commands
        parser.add_argument("-s", "--search", type=str, help="Search for torrent")
        parser.add_argument("-i", "--info", type=str, help="Get info on torrent")
        parser.add_argument("-up", "--uploader", type=str, help="Search by uploader")
        parser.add_argument("-desc", "--description", type=str, help="Search by description")
        parser.add_argument("-bdinfo", "--bdinfo", type=str, help="Show BDInfo")
        parser.add_argument("-m", "--mediainfo", type=str, help="Show MediaInfo")
        parser.add_argument("-st", "--startyear", type=str, help="Start year")
        parser.add_argument("-en", "--endyear", type=str, help="End year")
        parser.add_argument("-type", "--type", type=str, help="Filter by type")
        parser.add_argument("-res", "--resolution", type=str, help="Filter by resolution")
        parser.add_argument("-file", "--filename", type=str, help="Search by filename")

        parser.add_argument("-se", "--season", type=str, help="Season number")
        parser.add_argument("-ep", "--episode", type=str, help="Episode number")
        parser.add_argument("-tmdb", "--tmdb_id", type=str, help="TMDB ID")
        parser.add_argument("-imdb", "--imdb_id", type=str, help="IMDB ID")
        parser.add_argument("-tvdb", "--tvdb_id", type=int, help="TVDB ID")
        parser.add_argument("-mal", "--mal_id", type=str, help="MAL ID")

        parser.add_argument("-playid", "--playlist_id", type=str, help="Playlist ID")
        parser.add_argument("-coll", "--collection_id", type=str, help="Collection ID")
        parser.add_argument("-free", "--freelech", type=str, help="Freelech discount")

        # Torrent state commands
        parser.add_argument("-a", "--alive", action="store_true", help="Alive torrent")
        parser.add_argument("-d", "--dead", action="store_true", help="Dead torrent")
        parser.add_argument("-dy", "--dying", action="store_true", help="Dying torrent")

        parser.add_argument(
            "-du", "--doubleup", action="store_true", help="DoubleUp torrent"
        )
        parser.add_argument(
            "-fe", "--featured", action="store_true", help="Featured torrent"
        )
        parser.add_argument(
            "-re", "--refundable", action="store_true", help="Refundable torrent"
        )
        parser.add_argument(
            "-str", "--stream", action="store_true", help="Stream torrent"
        )
        parser.add_argument(
            "-sd", "--standard", action="store_true", help="Standard definition torrent"
        )
        parser.add_argument(
            "-hs", "--highspeed", action="store_true", help="Highspeed torrent"
        )
        parser.add_argument(
            "-int", "--internal", action="store_true", help="Internal torrent"
        )
        parser.add_argument(
            "-pers", "--personal", action="store_true", help="Personal release torrent"
        )

        self.args: parser = parser.parse_args()
        self.is_dir = os.path.isdir(self.args.scan) if self.args.scan else None

        # Check if the upload path is valid
        if self.args.upload and not os.path.exists(self.args.upload):
            custom_console.bot_error_log(f"The path {self.args.upload} does not exist.")
            sys.exit()
