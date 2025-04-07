# -*- coding: utf-8 -*-
import argparse
import os

from common.bittorrent import BittorrentData

from unit3dup.media_manager.common import UserContent
from unit3dup.pvtDocu import PdfImages
from unit3dup.upload import UploadBot
from unit3dup import config_settings
from unit3dup.media import Media

from view import custom_console

class DocuManager:

    def __init__(self, contents: list[Media], cli: argparse.Namespace):
        self._my_tmdb = None
        self.contents: list['Media'] = contents
        self.cli: argparse = cli

    def process(self, selected_tracker: str, tracker_name_list: list, tracker_archive: str) -> list[BittorrentData] | None:

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

            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker,
                                                 no_title=self.cli.notitle)):
                continue

            # Don't upload if -noup is set to True
            if self.cli.noup:
                custom_console.bot_warning_log(f"No Upload active. Done.")
                continue

            # Get the cover image
            docu_info = PdfImages(content.file_name)
            docu_info.build_info()

            # Tracker payload
            unit3d_up = UploadBot(content=content, tracker_name=selected_tracker)

            # Upload
            unit3d_up.data_docu(document_info=docu_info)

            # Get the data
            tracker_response, tracker_message = unit3d_up.send(torrent_archive=torrent_filepath)

            bittorrent_list.append(
                BittorrentData(
                    tracker_response=tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message=tracker_message,
                    archive_path=torrent_filepath,
                ))

        return bittorrent_list