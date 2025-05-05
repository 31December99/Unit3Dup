# -*- coding: utf-8 -*-
import argparse
import os

from common.bittorrent import BittorrentData, Payload

from unit3dup.media_manager.common import UserContent
from unit3dup.pvtDocu import PdfImages
from unit3dup.media import Media

from view import custom_console

class DocuManager:

    def __init__(self, contents: list[Media], cli: argparse.Namespace):
        self._my_tmdb = None
        self.contents: list['Media'] = contents
        self.cli: argparse = cli

    def process(self, selected_tracker: str, tracker_name_list: list, tracker_archive: str) -> list[BittorrentData]:

        # -multi : no announce_list . One announce for multi tracker
        if self.cli.mt:
            tracker_name_list = [selected_tracker.upper()]

        #  Init the torrent list
        bittorrent_list = []
        for content in self.contents:
            # get the archive path
            archive = os.path.join(tracker_archive, selected_tracker)
            os.makedirs(archive, exist_ok=True)
            torrent_filepath = os.path.join(tracker_archive,selected_tracker, f"{content.torrent_name}.torrent")

            if self.cli.watcher:
                if os.path.exists(content.torrent_path):
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                continue

            torrent_response = UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                   selected_tracker=selected_tracker, this_path=torrent_filepath)


            # print the title will be shown on the torrent page
            custom_console.bot_log(f"'DISPLAYNAME'...{{{content.display_name}}}\n")

            # Don't upload if -noup is set to True
            if self.cli.noup:
                custom_console.bot_warning_log(f"No Upload active. Done.")
                continue

            # Get the cover image
            docu_info = PdfImages(content.file_name)
            docu_info.build_info()

            payload = Payload(
                tracker_name=selected_tracker,
                cli=self.cli,
                show_id=None,
                show_keywords=None,
                video_info=None,
                imdb_id=None,
                igdb= None,
                docu_info= None
            )

            # Store response for the torrent clients
            bittorrent_list.append(
                BittorrentData(
                    tracker_response= None, # tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message = None, # tracker_message,
                    archive_path=torrent_filepath,
                    payload=payload
                ))

        # // end content
        return bittorrent_list