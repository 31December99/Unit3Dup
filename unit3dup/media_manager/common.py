# -*- coding: utf-8 -*-
import os
import bencode2
from concurrent.futures import ThreadPoolExecutor

from common.torrent_clients import TransmissionClient, QbittorrentClient
from common.trackers.data import trackers_api_data
from common.bittorrent import BittorrentData
from common.utility import ManageTitles
from common import config_settings

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.duplicate import Duplicate
from unit3dup.media import Media

from view import custom_console

class UserContent:
    """
    Manage user media Files
    """


    @staticmethod
    def torrent_announces(torrent_path: str, tracker_name_list: list):
        """ Add announces to a torrent file"""

        # // Read the existing torrent file
        with open(torrent_path, 'rb') as f:
            # It decodes it
            torrent_data = bencode2.bdecode(f.read())

        if not tracker_name_list:
            tracker_name_list = [config_settings.tracker_config.MULTI_TRACKER[0]]

        announce_list_encoded = []
        # a single tracker in the tracker_list corresponds to the '-tracker' flag from the user's CLI
        # two or more trackers in the tracker_list correspond to the '-cross' flag from the user's CLI
        for tracker in tracker_name_list:
            # Get data for each tracker
            api_data = trackers_api_data[tracker.upper()]
            # Add to the list and encode it
            announce_list_encoded.append([api_data['announce'].encode()])

        if b'announce-list' in torrent_data:

            # Edit the announce list only if it is different from the announce_list_encoded (user CLI)
            if torrent_data[b'announce-list'] != announce_list_encoded:
                custom_console.bot_warning_log("BEFORE:")
                for announce in torrent_data[b'announce-list']:
                    custom_console.bot_log(f"{announce[0].decode()[:-32]}{'*' * 32}")

                custom_console.bot_warning_log("AFTER:")
                if not announce_list_encoded:
                    custom_console.bot_log(f"Default tracker selected"
                                           f" '{config_settings.tracker_config.MULTI_TRACKER[0].upper()}'")

                else:
                    for announce in announce_list_encoded:
                        custom_console.bot_log(f"{announce[0].decode()[:-32]}{'*' * 32}")
                del torrent_data[b'announce-list']

        if b'announce' in torrent_data:
            if torrent_data[b'announce'] != announce_list_encoded:
                custom_console.bot_warning_log("BEFORE:")
                custom_console.bot_log(f"{torrent_data[b'announce'].decode()}")
                custom_console.bot_warning_log("AFTER:")
                if not announce_list_encoded:
                    custom_console.bot_log(f"Default tracker selected"
                                           f" '{config_settings.tracker_config.MULTI_TRACKER[0].upper()}'")
                else:
                    custom_console.bot_log(announce_list_encoded)
                del torrent_data[b'announce']

        # Set the new announce list
        torrent_data[b'announce-list'] = announce_list_encoded

        # // Save
        with open(torrent_path, 'wb') as f:
            f.write(bencode2.bencode(torrent_data))
        print()


    @staticmethod
    def torrent_file_exists(path: str, tracker_name_list: list) -> bool:
        """
        Check if a torrent file for the given content already exists

        Args:
            path: The torrent's path
            tracker_name_list: the trackers name

        Returns:
            bool: True if the torrent file exists otherwise False
        """

        base_name = os.path.basename(path)

        if config_settings.user_preferences.TORRENT_ARCHIVE_PATH:
            this_path = os.path.join(config_settings.user_preferences.TORRENT_ARCHIVE_PATH, f"{base_name}.torrent")
        else:
            this_path = f"{path}.torrent"

        if os.path.exists(this_path):
            custom_console.bot_warning_log(
                f"** {UserContent.__class__.__name__} **: Reusing the existing torrent file! {this_path}\n"
            )

            # Add an announce_list or remove 'announce-list' if the list is empty
            UserContent.torrent_announces(torrent_path=this_path, tracker_name_list=tracker_name_list)
            return True
        return False


    @staticmethod
    def is_preferred_language(content: Media) -> bool:
        """
           Compare preferred language with the audio language

           Args:
               content (Contents): The content object media

           Returns:
               return boolean
           """
        preferred_lang = config_settings.user_preferences.PREFERRED_LANG.upper()
        preferred_lang_to_iso = ManageTitles.convert_iso(preferred_lang)

        if not content.audio_languages:
            return True

        if preferred_lang == 'ALL':
            return True

        if preferred_lang_to_iso in content.audio_languages:
            return True

        custom_console.bot_log(f"'{content.file_name}'")
        custom_console.bot_warning_log(
            "[UserContent] ** Your preferred lang is not in your media being uploaded, skipping ! **\n"
        )
        custom_console.rule()
        return False

    @staticmethod
    def torrent(content: Media, trackers: list)-> Mytorrent:
        """
           Create the file torrent

           Args:
               content (Contents): The content object media
               trackers: list of name of the trackers

           Returns:
               my_torrent object
        """

        # Add announcement only if expressly requested by the user via cli -tracker flag
        my_torrent = Mytorrent(contents=content, meta=content.metainfo, trackers_list=trackers)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    @staticmethod
    def is_duplicate(content: Media, tracker_name: str) -> bool:
        """
           Search for a duplicate. Delta = config.SIZE_TH

           Args:
               content (Contents): The content object media
               tracker_name: The name of the tracker

           Returns:
               my_torrent object
        """

        duplicate = Duplicate(content=content, tracker_name=tracker_name)
        if duplicate.process():
            custom_console.bot_error_log(
                f"\n*** User chose to skip '{content.display_name}' ***\n"
            )
            custom_console.rule()
            return True
        else:
            return False


    @staticmethod
    def send_to_bittorrent_worker(bittorrent_file: BittorrentData, client: QbittorrentClient | TransmissionClient):
        """
        worker: This function will handle sending a single torrent to torrent clients

        Args:
            bittorrent_file: The object containing the torrent and other necessary info
            client: qbittorrent client | transmission_rpc
        """
        try:
            # Check if we have a valid response from the tracker
            if bittorrent_file.tracker_response:
                if client:
                    client.send_to_client(
                    tracker_data_response=bittorrent_file.tracker_response,
                    torrent=bittorrent_file.torrent_response,
                    content=bittorrent_file.content,
                )
            else:
                # invalid response
                custom_console.bot_error_log(f"[{bittorrent_file.content.display_name}] ->"
                                       f" {bittorrent_file.tracker_message}")
        except Exception as e:
            custom_console.bot_error_log(f"Error sending torrent {bittorrent_file.content.file_name}: {str(e)}")


    @staticmethod
    def get_client() -> QbittorrentClient | TransmissionClient:

        client = QbittorrentClient()

        if config_settings.torrent_client_config.TORRENT_CLIENT.lower()=='qbittorrent':
            client = QbittorrentClient()
            client.connect()

        elif config_settings.torrent_client_config.TORRENT_CLIENT.lower()=='transmission':
            client = TransmissionClient()
            client.connect()
        else:
            custom_console.bot_error_log(f"{UserContent.__class__.__name__}"
                                         f" Invalid torrent client '{config_settings.torrent_client_config.TORRENT_CLIENT}'" )
            exit(1)

        return client

    @staticmethod
    def send_to_bittorrent(bittorrent_list: list[BittorrentData]) -> None:
        """
        Sends a list of torrents to qBittorrent using threads ( async later...)

        Args:
            bittorrent_list (list[Bittorrent]): A list of Bittorrent objects to be sent to the client
        """

        if not bittorrent_list:
            return None

        custom_console.bot_warning_log(f"\nSending torrents to the client "
                                       f"{config_settings.torrent_client_config.TORRENT_CLIENT.upper()}"
                                       f"... Please wait")

        client = QbittorrentClient()

        if config_settings.torrent_client_config.TORRENT_CLIENT.lower()=='qbittorrent':
            client = QbittorrentClient()
            client.connect()

        elif config_settings.torrent_client_config.TORRENT_CLIENT.lower()=='transmission':
            client = TransmissionClient()
            client.connect()
        else:
            custom_console.bot_error_log(f"{UserContent.__class__.__name__}"
                                         f" Invalid torrent client '{config_settings.torrent_client_config.TORRENT_CLIENT}'" )
            exit(1)

        with ThreadPoolExecutor(max_workers=20) as executor:
            # Submit the torrents
            futures = [executor.submit(UserContent.send_to_bittorrent_worker, bittor, client)
                       for bittor in bittorrent_list]
            # Wait for all threads to complete
            for future in futures:
                future.result()