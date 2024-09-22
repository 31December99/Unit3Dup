# -*- coding: utf-8 -*-

import argparse

from common.external_services.theMovieDB.tmdb_service import TmdbService
from common.external_services.ftpx.core.models.list import FTPDirectory
from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.TorrentManager import TorrentManager
from common.external_services.Pw.pw_service import PwService
from common.external_services.ftpx.core.menu import Menu
from common.external_services.ftpx.client import Client
from common.custom_console import custom_console
from common.extractor import Extractor
from common.config import config

from common.external_services.igdb.client import IGdbServiceApi


class Bot:
    """
    A class to manage and execute media-related tasks including file processing,
    torrent management, and interaction with the TMDB service.
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

        # Torrent Manager
        self.torrent_manager = TorrentManager(cli=self.cli)

        # TMDB service
        self.tmdb_service = TmdbService()

    def run(self) -> None:
        """
        Start the process
        """
        custom_console.panel_message("Analyzing... Please wait")

        # Get user contents
        self.content_manager = ContentManager(
            path=self.path, tracker_name=self.tracker_name, mode=self.mode
        )

        # Get the contents
        files = self.content_manager.get_files()

        # Search for rar files and decompress them
        extractor = Extractor(media=files)

        result = extractor.unrar()
        if result is False:
            exit(1)

        # Create the file objects
        contents = [
            content
            for item in files
            if (content := self.content_manager.get_media(item))
        ]
        # Print the list of selected files being processed
        custom_console.bot_process_table_log(contents)

        # Process them
        self.torrent_manager.process(contents)

    def pw(self):
        # PW service
        if not config.PW_API_KEY:
            return

        pw_service = PwService()
        custom_console.panel_message("Analyzing... Please wait")
        # Examples

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
        custom_console.bot_question_log("\nConnecting to the remote FTP...")

        if not config.FTPX_LOCAL_PATH:
            custom_console.bot_error_log(
                "Set FTPX_LOCAL_PATH for -ftp command. Exit..."
            )
            exit(1)

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

        # Return the path for the upload
        if ftp_client.download_to_local_path:
            scan_path = ftp_client.download_to_local_path.split("/")
            scan_path = "/".join(scan_path[:-1])
            self.path = scan_path
            self.run()

    def igdb(self):


        #IGDB service
        self.ig_db = IGdbServiceApi()
        self.ig_db.login()
        print(self.ig_db.request("Lineage"))




