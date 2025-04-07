# -*- coding: utf-8 -*-

import argparse
import os

from common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.media_manager.common import UserContent
from unit3dup.media import Media
from unit3dup.torrent import Torrent

from common.bittorrent import BittorrentData
from common import title

from view import custom_console

class SeedManager:
    def __init__(self, contents: list[Media], cli: argparse.Namespace):

         self.contents = contents
         # Command line
         self.cli = cli

    def process(self, selected_tracker: str, trackers_name_list: list, tracker_archive: str) -> list[BittorrentData] | None:

        # Tracker new instance
        torrent_info = Torrent(tracker_name=selected_tracker)

        # Data list for the torrent client
        bittorrent_list = []

        # Iterate user content
        if self.contents:
            for content in self.contents:
                # get the archive path
                archive = os.path.join(tracker_archive, selected_tracker)
                # Build the path for downloading
                os.makedirs(archive, exist_ok=True)
                torrent_filepath = os.path.join(tracker_archive, selected_tracker, f"{content.torrent_name}.torrent")
                # Search for tmdb ID
                db_online = DbOnline(media=content, category=content.category, no_title=self.cli.notitle)
                db = db_online.media_result
                # Search a torrent based on TMDB ID
                filter_tmdb = torrent_info.get_by_tmdb_id(tmdb_id=db.video_id)
                # Get a list of urls based on TMDB ID
                tracker_download_urls = self.death(tmdb_list=filter_tmdb, content=content,
                                                  selected_tracker=selected_tracker)
                # Create a list di BittorrentData
                if tracker_download_urls:
                        for tracker_download_url in tracker_download_urls:
                            bittorrent_list.append(BittorrentData(
                                tracker_response=tracker_download_url,
                                torrent_response=None,
                                content=content,
                                tracker_message={},
                                archive_path=torrent_filepath,
                            ))

        return bittorrent_list


    def death(self, tmdb_list, content: Media, selected_tracker: str) -> list:

        for dead in tmdb_list['data']:
            custom_console.bot_log(f"'(Dead)' {dead['attributes']['name']}")
        print()
        tracker_download_urls = []

        for dead in tmdb_list['data']:
            # Read the remote torrent data
            tracker_title = title.Guessit(dead['attributes']['name'])
            tracker_download_url = dead['attributes']['download_link']
            tracker_title_season = tracker_title.guessit_season
            tracker_title_episode = tracker_title.guessit_episode
            # Check Season and Episode ( None if it's movie)
            if tracker_title_season == content.guess_season and tracker_title_episode == content.guess_episode:
                # Search only for duplicates that are torrent files matching the local file to download and reseed
                if not UserContent.is_duplicate(content=content, tracker_name=selected_tracker,no_title=self.cli.notitle):
                    custom_console.bot_warning_log(f"'RESEED'........ {dead['attributes']['name']}:"
                                                   f" {dead['attributes']['details_link']}\n")
                    # Create a list of torrent url
                    tracker_download_urls.append(tracker_download_url)
        print()
        return tracker_download_urls



