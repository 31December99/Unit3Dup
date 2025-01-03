# -*- coding: utf-8 -*-

import argparse
import os
import time
import shutil

from pathlib import Path
from common.external_services.theMovieDB.tmdb_service import TmdbService
from common.external_services.ftpx.core.models.list import FTPDirectory
from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.TorrentManager import TorrentManager
from common.external_services.Pw.pw_service import PwService
from common.external_services.ftpx.core.menu import Menu
from common.external_services.ftpx.client import Client
from common.custom_console import custom_console
from common.extractor import Extractor


class Bot:
    """
    A class to manage and execute media-related tasks including file processing,
    torrent management, and interaction with the TMDB service
    """

    def __init__(
            self, path: str, tracker_name: str, cli: argparse.Namespace, mode="man"
    ):
        """
        Initialize the Bot instance with path, tracker name, command-line interface object, and mode

        Args:
            path (str): The path to the directory or file to be managed
            tracker_name (str): The name of the tracker configuration to use
            cli (argparse.Namespace): The command-line arguments object
            mode (str): The mode of operation, default is 'man'
        """
        self.content_manager = None
        self.path = path
        self.tracker_name = tracker_name
        self.cli = cli
        self.mode = mode

        # Bot Manager
        self.torrent_manager = TorrentManager(cli=self.cli)

        # TMDB service
        # self.tmdb_service = TmdbService()

    def run(self) -> None:
        """
        Start the process
        """
        custom_console.panel_message("Analyzing your media files... Please wait")

        # Get Files list with basic attributes
        # from the upload() or scan command()
        # and create an object Media
        # torrent_path
        # media_type
        # crew
        # game_tags
        # game_title
        self.content_manager = ContentManager(
            path=self.path, tracker_name=self.tracker_name, mode=self.mode
        )
        file_media_list = self.content_manager.get_files()

        if not file_media_list:
            custom_console.bot_error_log("There are no files to process")
            return

        # Decompress the rar files( only for ftp or -unrar flag)
        if self.cli.ftp or self.cli.unrar:
            extractor = Extractor(media=file_media_list)
            result = extractor.unrar()
            if result is False:
                custom_console.bot_error_log("Unrar Exit")
                exit(1)

        # Create an object Files for each file from the files_list
        # We need to prepare each file (Files class) to create a content object (Contents):

        # file without folder
        # file with folder
        # folder with files
        # tv show title string
        # movie title string
        # display_name for the tracker website string
        # media_info json
        # game by crew
        # game title for query igdb
        # game tags (platform) for query igdb
        # document
        # doc description
        # torrent package
        # torrent name
        # torrent file name
        # torrent meta_file
        # torrent size (field)
        # audio languages

        # Media > Files > Content
        contents = [
            content
            for media in file_media_list
            if (content := self.content_manager.get_media(media))
        ]

        # Print the list of selected files being processed
        # the contents objects
        custom_console.bot_process_table_log(contents)

        # Process them
        self.torrent_manager.process(contents)

    def watcher(self, duration: int, watcher_path: str):

        # Watchdog loop
        while True:
            start_time = time.perf_counter()
            end_time = start_time + duration

            # return if there are no file
            if not os.path.exists(watcher_path) or not os.listdir(watcher_path):
                return

            print()
            # Counter
            while time.perf_counter() < end_time:
                remaining_time = end_time - time.perf_counter()
                custom_console.bot_counter_log(f"WATCHDOG: {remaining_time:.1f} seconds")
                time.sleep(0.01)
            print()

            # Scan the source ( watcher_path) and move each file into the destination folder
            for root, dirs, files in os.walk(watcher_path):
                dest_root = Path(root.replace(watcher_path, self.path))
                dest_root.mkdir(parents=True, exist_ok=True)

                for file_name in files:
                    src_file = Path(root) / file_name
                    dest_file = dest_root / file_name

                    # limits string too long
                    limiter_src = '...' if len(str(src_file)) > 50 else ''
                    limiter_dest = '...' if len(str(dest_file)) > 50 else ''

                    custom_console.bot_log(f"{str(src_file)[:50]}{limiter_src} -> from 'watch folder' to 'destination folder'"
                                           f" -> {str(dest_file)[:50]}{limiter_dest}")
                    shutil.move(str(src_file), str(dest_file))  # Sposta il file

                if root != watcher_path and not os.listdir(root):
                    try:
                        os.rmdir(root)
                    except OSError as e:
                        custom_console.bot_error_log(e)
                        exit()

            # Start uploading process
            print()
            self.run()

    def pw(self):

        # PW service
        pw_service = PwService()
        custom_console.panel_message("Analyzing... Please wait")
        # Examples Test

        """
        # Now Playing by country
        releases_latest = self.tmdb_service.latest_movie_by_country(country_code="IT")
        custom_console.log(releases_latest)
        custom_console.rule()

        # Alternative title for a movie
        alternative_title = self.tmdb_service.movie_alternative_title(movie_id=533535)
        custom_console.log(alternative_title)
        custom_console.rule()

        # Search for a movie title
        search_movie = self.tmdb_service.search_movies(query="Blade Runner 2049")
        custom_console.log(search_movie)
        custom_console.rule()

        # On The Air by country
        tv_shows = self.tmdb_service.latest_show_by_country(country_code="IT")
        custom_console.log(tv_shows)
        custom_console.rule()

        # Tv Show Details by ID
        tv_show_details = self.tmdb_service.tv_show_details(tv_show_id=84773)
        custom_console.log(tv_show_details)
        custom_console.rule()

        # Search for a tv show title
        search_tv_show = self.tmdb_service.search_tv_show(
            query="Il Signore degli Anelli: Gli Anelli del Potere"
        )
        custom_console.log(search_tv_show)
        custom_console.rule()

        # Get PW indexers
        indexers = self.pw_service.get_indexers()
        custom_console.log(indexers)
        """

        # Query the indexers
        search = pw_service.search(query="Maze runner")
        for index, s in enumerate(search):
            if s.seeders > 1:
                torrent_file = search[index]
                custom_console.log(torrent_file)

    def ftp(self):
        """
        Controller
        """
        custom_console.bot_question_log("\nConnecting to the remote FTP...\n")

        # FTP service
        ftp_client = Client()
        custom_console.bot_question_log(f"Connected to {ftp_client.sys_info()}\n\n")

        menu = Menu()

        page = ftp_client.home_page()
        menu.show(table=page)

        while 1:
            user_option = ftp_client.user_input()
            # return a table(page) or a selected folder (FTPDirectory)
            page = ftp_client.input_manager(user_option)
            if page == 0:
                ftp_client.quit()
                break
            if not page:
                continue

            # Display the page as FtpDirectory (user choice)
            if isinstance(page, FTPDirectory):
                ftp_directory_name = page.name
                # Change the path based on the user choice
                if page.type == "Folder":
                    page = ftp_client.change_path(selected_folder=ftp_directory_name)
                    menu.show(table=page)
                else:
                    ftp_client.select_file(one_file_selected=page)
                continue

            # Display the page as table
            menu.show(table=page)

        if ftp_client.download_to_local_path:
            # Get only the folder part for the scanning process
            self.path = os.path.dirname(ftp_client.download_to_local_path)
            # Upload -f process
            self.run()
