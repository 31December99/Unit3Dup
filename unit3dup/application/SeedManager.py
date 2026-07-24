# -*- coding: utf-8 -*-

import os

from unit3dup.external.theMovieDB.core.api import DbOnline
from unit3dup.external.torrent.bittorrent import BittorrentData
from unit3dup.external.media import Media

from unit3dup.application.user_content import UserContent
from unit3dup.config.bot_config import BotConfig


class SeedManager:
    def __init__(self, contents: list[Media], cli: BotConfig):

        self.contents = contents
        # Command line
        self.cli: BotConfig = cli

    def process(self, selected_tracker: str, trackers_name_list: list, tracker_archive: str) -> list[
                                                                                                    BittorrentData] | None:

        # Data list for the torrent client
        bittorrent_list = []

        # Iterate user content
        if self.contents:
            for content in self.contents:
                # get the archive path
                archive = os.path.join(tracker_archive, selected_tracker)
                # Build the path for downloading
                os.makedirs(archive, exist_ok=True)
                content.torrent_metadata_path = os.path.join(tracker_archive, selected_tracker, f"{content.torrent_name}.torrent")
                # Search for tmdb ID
                db_online = DbOnline(media=content, no_title=self.cli.notitle)
                content.media_result = db_online.media_result

                torrents = UserContent.can_ressed(content=content, tracker_name=selected_tracker, cli=self.cli,
                                                  tmdb_id=content.media_result.video_id)

                for t in torrents:
                    bittorrent_list.append(BittorrentData(
                        tracker_response=t['attributes']['download_link'],
                        content=content,
                        tracker_message={},
                        archive_path=content.torrent_metadata_path,
                    ))

            return bittorrent_list
        return None
