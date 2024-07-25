# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
import sys
from rich.console import Console

from unit3dup.uploader import UploadBot
from unit3dup.utility import Manage_titles
from unit3dup.contents import Contents, File, Folder
from unit3dup.config import ConfigUnit3D
from unit3dup import Torrent
from unit3dup import title

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

        self.tracker: str = self.args.tracker
        self.path: str = self.args.scan
        self.is_dir = os.path.isdir(self.path) if self.path else None

        if self.args.upload and not os.path.exists(self.args.upload):
            console.log(f"The path {self.args.upload} does not exist.")
            sys.exit()

        if not os.path.exists(f"{self.tracker}.env"):
            console.log(
                f"Configuration file '{self.tracker}.env' not found for tracker '{self.tracker}'"
            )
            sys.exit()

        if not os.path.exists(f"{self.tracker}.json"):
            console.log(
                f"Configuration file '{self.tracker}.json' not found for tracker '{self.tracker}'"
            )
            sys.exit()

    @staticmethod
    def config_load():
        try:
            config_unit3d = ConfigUnit3D.validate(
                tracker_env_name="itt.env", service_env_name="service.env"
            )
        except FileNotFoundError as message:
            console.log(message)

    @staticmethod
    def welcome_message(message: str):
        if message:
            console.rule(f"[bold blue]{message.upper()}", style="#ea00d9")


class Video:
    """
    e identificare quelli che sono i files(movies) e i folder(series)

    """

    def __init__(self, path: str, tracker: str):
        self.meta_info_list: list = []
        self.meta_info = None
        self.size = None
        self.name = None
        self.category = None
        self.folder = None
        self.file_name = None
        self.tracker: str = tracker
        self.path: str = path
        self.movies: list = []
        self.series: list = []
        self.is_dir = os.path.isdir(self.path)
        console.log(f"IS DIR {self.is_dir}")

    def get_data(self) -> Contents | bool:
        """
        Create an userinput object with movie or series attributes for the torrent.
        Verify if name is part of torrent pack folder. If there is no episode it's a pack
        """
        if not self.is_dir:
            # Check for valid extension
            process = (
                self.process_file() if Manage_titles.filter_ext(self.path) else False
            )
        else:
            process = self.process_folder()

        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))
        console.log(f"\n[TORRENT PACK] {torrent_pack}...  '{self.path}'")

        return (
            Contents.create_instance(
                file_name=self.file_name,
                folder=self.folder,
                name=self.name,
                size=self.size,
                metainfo=self.meta_info,
                category=self.category,
                tracker_name=self.tracker,
                torrent_pack=torrent_pack,
            )
            if process
            else False
        )

    def process_file(self) -> bool:
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.category = 1
        self.name, ext = os.path.splitext(self.file_name)
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps(
            [{"length": self.size, "path": [self.file_name]}], indent=4
        )
        return True

    def process_folder(self) -> bool:
        files = self.list_video_files()
        if not files:
            console.log(
                f"\n*** '{self.path}' No video files found in the directory - skip ***\n"
            )
            return False

        self.file_name = files[0]
        self.folder = self.path
        self.category = 2
        self.name, ext = os.path.splitext(self.file_name)

        self.meta_info_list = []
        total_size = 0
        for file in files:
            size = os.path.getsize(os.path.join(self.folder, file))
            self.meta_info_list.append({"length": size, "path": [file]})
            total_size += size
        self.size = total_size
        self.meta_info = json.dumps(self.meta_info_list, indent=4)
        return True

    def list_video_files(self) -> list:
        """
        Add to the list every file if its extension is in the video_ext.
        """
        return [
            file for file in os.listdir(self.path) if Manage_titles.filter_ext(file)
        ]


class Auto:

    def __init__(self, path: str):
        self.series = None
        self.movies = None
        self.path = path

    def scan(self):
        movies_path = []
        series_path = []

        for path, sub_dirs, files in os.walk(self.path):
            if path == self.path:
                movies_path = [
                    os.path.join(self.path, file)
                    for file in files
                    if Manage_titles.filter_ext(file)
                ]
            if sub_dirs:
                # Maximum level of subfolder depth = 1
                if self.depth_walker(path) < 1:
                    series_path = [
                        os.path.join(self.path, subdir) for subdir in sub_dirs
                    ]

        self.movies = [
            self.create_movies_path(file)
            for file in movies_path
            if self.create_movies_path(file) is not None
        ]
        # None in the series means a folder without an Sx tag
        self.series = [self.create_series_path(subdir) for subdir in series_path]
        return self.series, self.movies

    def create_movies_path(self, file: str) -> File | None:
        """
        Determines if it is a movie or a series. Excludes any episode files.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)
        if not guess_filename.guessit_season:
            return File.create(file_name=file, folder=self.path, media_type="1")
        else:
            return None

    def create_series_path(self, subdir: str) -> Folder | None:
        """
        Determines whether the folder contains an Sx tag
        """
        file_name, ext = os.path.splitext(subdir)
        guess_filename = title.Guessit(file_name)
        if guess_filename.guessit_season:
            return Folder.create(folder=self.path, subfolder=subdir, media_type="2")
        else:
            return None

    def depth_walker(self, path) -> int:
        """
        It stops at one subfolder and ignores any subfolders within that subfolder
        depth < 1
        """
        return path[len(self.path) :].count(os.sep)


def main():
    cli = CommandLine()
    cli.config_load()

    if cli.args.scan:
        auto = Auto(cli.path)
        series, movies = auto.scan()

        for item in series + movies:
            video = Video(path=item.torrent_path, tracker=cli.tracker)
            content = video.get_data()
            bot = UploadBot(content)

            if bot.category == 1:
                data = bot.movie_data()
                bot.process_data(data)
            else:
                data = bot.serie_data()
                bot.process_data(data)

        """
            COMMANDS LIST: commands not necessary for the upload but may be useful
        """

    torrent_info = Torrent(cli.tracker)

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
