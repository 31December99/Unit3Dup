# -*- coding: utf-8 -*-
"""
CLI command handlers separated from main entrypoint.

This module contains the business logic for each CLI command,
separated from the argument parsing and initialization logic.
"""

from typing import List
import sys

from common.torrent_clients import TransmissionClient, QbittorrentClient, RTorrentClient
from common.config_manager import get_config
from unit3dup.bot import Bot
from unit3dup.torrent import View
from view import custom_console


class CLICommands:
    """Handles execution of CLI commands."""
    
    def __init__(self, cli_args, tracker_name_list: List[str], tracker_archive: str):
        """
        Initialize CLI command handler.
        
        Args:
            cli_args: Parsed command line arguments
            tracker_name_list: List of tracker names to use
            tracker_archive: Path to torrent archive
        """
        self.cli_args = cli_args
        self.tracker_name_list = tracker_name_list
        self.tracker_archive = tracker_archive
        self.config = get_config()
    
    def execute_upload_command(self) -> None:
        """Execute manual upload mode."""
        bot = Bot(
            path=self.cli_args.upload,
            cli=self.cli_args,
            trackers_name_list=self.tracker_name_list,
            torrent_archive_path=self.tracker_archive
        )
        bot.run()
    
    def execute_folder_command(self) -> None:
        """Execute manual folder mode."""
        bot = Bot(
            path=self.cli_args.folder,
            cli=self.cli_args,
            mode="folder",
            trackers_name_list=self.tracker_name_list,
            torrent_archive_path=self.tracker_archive,
        )
        bot.run()
    
    def execute_scan_command(self) -> None:
        """Execute auto scan mode."""
        bot = Bot(
            path=self.cli_args.scan,
            cli=self.cli_args,
            mode="auto",
            trackers_name_list=self.tracker_name_list,
            torrent_archive_path=self.tracker_archive
        )
        bot.run()
    
    def execute_watcher_command(self) -> None:
        """Execute watcher mode."""
        bot = Bot(
            path='',
            cli=self.cli_args,
            mode="auto",
            trackers_name_list=self.tracker_name_list,
            torrent_archive_path=self.tracker_archive
        )
        bot.watcher(
            duration=self.config.user_preferences.WATCHER_INTERVAL,
            watcher_path=self.config.user_preferences.WATCHER_PATH,
            destination_path=self.config.user_preferences.WATCHER_DESTINATION_PATH
        )
    
    def execute_ftp_command(self) -> None:
        """Execute FTP mode."""
        bot = Bot(
            path='',
            cli=self.cli_args,
            mode="folder",
            trackers_name_list=self.tracker_name_list
        )
        bot.ftp()
    
    def execute_query_commands(self) -> None:
        """
        Execute torrent query/search commands.
        
        These commands don't upload but query the tracker API.
        """
        if not self.cli_args.tracker:
            return
        
        torrent_info = View(tracker_name=self.cli_args.tracker)
        
        # Filter combo: TMDB + resolution
        if self.cli_args.tmdb_id and self.cli_args.resolution:
            torrent_info.view_tmdb_res(self.cli_args.tmdb_id, self.cli_args.resolution)
            return
        
        # Individual query commands
        query_map = {
            'search': lambda: torrent_info.view_search(self.cli_args.search, save=self.cli_args.dbsave),
            'info': lambda: torrent_info.view_search(self.cli_args.info, info=True),
            'description': lambda: torrent_info.view_by_description(self.cli_args.description),
            'bdinfo': lambda: torrent_info.view_by_bdinfo(self.cli_args.bdinfo),
            'uploader': lambda: torrent_info.view_by_uploader(self.cli_args.uploader),
            'startyear': lambda: torrent_info.view_by_start_year(self.cli_args.startyear),
            'endyear': lambda: torrent_info.view_by_end_year(self.cli_args.endyear),
            'type': lambda: torrent_info.view_by_types(self.cli_args.type),
            'resolution': lambda: torrent_info.view_by_res(self.cli_args.resolution),
            'filename': lambda: torrent_info.view_by_filename(self.cli_args.filename),
            'tmdb_id': lambda: torrent_info.view_by_tmdb_id(self.cli_args.tmdb_id),
            'imdb_id': lambda: torrent_info.view_by_imdb_id(self.cli_args.imdb_id),
            'tvdb_id': lambda: torrent_info.view_by_tvdb_id(self.cli_args.tvdb_id),
            'mal_id': lambda: torrent_info.view_by_mal_id(self.cli_args.mal_id),
            'playlist_id': lambda: torrent_info.view_by_playlist_id(self.cli_args.playlist_id),
            'collection_id': lambda: torrent_info.view_by_collection_id(self.cli_args.collection_id),
            'freelech': lambda: torrent_info.view_by_freeleech(self.cli_args.freelech),
            'season': lambda: torrent_info.view_by_season(self.cli_args.season),
            'episode': lambda: torrent_info.view_by_episode(self.cli_args.episode),
            'mediainfo': lambda: torrent_info.view_by_mediainfo(self.cli_args.mediainfo),
            'alive': lambda: torrent_info.view_alive(),
            'dead': lambda: torrent_info.view_dead(),
            'dying': lambda: torrent_info.view_dying(),
            'doubleup': lambda: torrent_info.view_doubleup(),
            'featured': lambda: torrent_info.view_featured(),
            'refundable': lambda: torrent_info.view_refundable(),
            'stream': lambda: torrent_info.view_stream(),
            'standard': lambda: torrent_info.view_sd(),
            'highspeed': lambda: torrent_info.view_highspeed(),
            'internal': lambda: torrent_info.view_internal(),
            'prelease': lambda: torrent_info.view_personal(),
        }
        
        # Execute the first matching command
        for arg_name, handler in query_map.items():
            if getattr(self.cli_args, arg_name, None):
                handler()
                return
        
        # Handle dump command
        if self.cli_args.dump:
            custom_console.print("NOT YET IMPLEMENTED")
            return


def validate_torrent_client(config) -> bool:
    """
    Validate and test torrent client connection.
    
    Args:
        config: Application configuration
        
    Returns:
        bool: True if client is available and connected, False otherwise
    """
    client_name = config.torrent_client_config.TORRENT_CLIENT.lower()
    
    client_map = {
        'qbittorrent': QbittorrentClient,
        'transmission': TransmissionClient,
        'rtorrent': RTorrentClient,
    }
    
    client_class = client_map.get(client_name)
    
    if not client_class:
        custom_console.bot_error_log(
            f"Unknown Torrent Client name '{config.torrent_client_config.TORRENT_CLIENT}'"
        )
        custom_console.bot_error_log(
            "You need to set a favorite 'torrent_client' in the config file"
        )
        return False
    
    test_client = client_class()
    if not test_client.connect():
        return False
    
    return True
