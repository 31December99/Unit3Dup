# -*- coding: utf-8 -*-
import argparse

from common.bittorrent import BittorrentData

from unit3dup.media_manager.common import UserContent
from unit3dup.pvtDocu import PdfImages
from unit3dup.upload import UploadBot
from unit3dup import config_settings
from unit3dup.media import Media

from view import custom_console

class DocuManager:

    def __init__(self, contents: list["Media"], cli: argparse.Namespace):
        self._my_tmdb = None
        self.contents: list['Media'] = contents
        self.cli: argparse = cli


    def process(self, selected_tracker:str, tracker_name_list: list) -> list["BittorrentData"]:
        bittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(path=content.torrent_path, tracker_name_list=tracker_name_list):
                torrent_response = UserContent.torrent(content=content, trackers=tracker_name_list)
            else:
                # Torrent found, skip if the watcher is active
                if self.cli.watcher:
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue
                torrent_response = None

            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                continue

            # Don't upload if -noup is set to True
            if self.cli.noup:
                custom_console.bot_warning_log(f"No Upload active. Done.")
                return []

            # Get the cover image
            docu_info = PdfImages(content.file_name)
            docu_info.build_info()

            # Tracker payload
            unit3d_up = UploadBot(content=content, tracker_name=selected_tracker)

            # Upload
            tracker_response, tracker_message = unit3d_up.send_docu(document_info=docu_info)

            bittorrent_list.append(
                BittorrentData(
                    tracker_response=tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message=tracker_message,
                ))

        return bittorrent_list