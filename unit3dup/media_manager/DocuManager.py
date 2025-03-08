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
        self.torrent_found: bool = False


    def process(self, selected_tracker:str) -> list["BittorrentData"]:
        bittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                self.torrent_found = False
            else:
                # Torrent found, skip if the watcher is active
                if self.cli.watcher:
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue
                self.torrent_found = True

            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                continue

            # Does not create the torrent if the torrent was found earlier
            if not self.torrent_found:
                torrent_response = UserContent.torrent(content=content)
            else:
                torrent_response = None

            # Get the cover image
            docu_info = PdfImages(content.file_name)
            docu_info.build_info()

            # Tracker payload
            if not self.cli.noupload:
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