# -*- coding: utf-8 -*-

import argparse
import os

from common.external_services.theMovieDB.core.api import DbOnline
from common.bittorrent import BittorrentData, Payload

from unit3dup.media_manager.common import UserContent
from unit3dup.media import Media

class SeedManager:
    def __init__(self, contents: list[Media], cli: argparse.Namespace):

         self.contents = contents
         # Command line
         self.cli = cli

    async def process(self, selected_tracker: str, trackers_name_list: list, tracker_archive: str) -> list[BittorrentData] | None:

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

                torrents = await UserContent.can_ressed(content=content, tracker_name=selected_tracker,cli=self.cli,
                                                  tmdb_id=db.video_id)
                for t in torrents:
                    payload = Payload(
                        tracker_name=selected_tracker,
                        cli=self.cli,
                        show_id=db.video_id,
                        show_keywords=db.keywords_list,
                        video_info=None,
                        imdb_id=db.imdb_id,
                        igdb=None,
                        docu_info=None
                    )

                    bittorrent_list.append(BittorrentData(
                        tracker_response=t['attributes']['download_link'],
                        torrent_response=None,
                        content=content,
                        tracker_message={},
                        archive_path=torrent_filepath,
                        payload=payload
                    ))

            return bittorrent_list
        return None
