# -*- coding: utf-8 -*-

import os
import time

import requests
import qbittorrent
import transmission_rpc
from abc import ABC, abstractmethod

from unit3dup.pvtTorrent import Mytorrent
from unit3dup import config_settings
from unit3dup.media import Media

from view import custom_console


class TorrClient(ABC):

    def __init__(self):
        self.client = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media, archive_path: str):
        pass

    def download(self, tracker_torrent_url: requests, torrent_path: str):
        # Archive the torrent file if torrent_archive is set
        if config_settings.user_preferences.TORRENT_ARCHIVE_PATH:
            file_name = f"{os.path.basename(torrent_path)}.torrent"
            full_path_archive = os.path.join(config_settings.user_preferences.TORRENT_ARCHIVE_PATH, file_name)
        else:
            # Or save to the current path
            full_path_archive = f"{torrent_path}.torrent"

        # File archived
        with open(full_path_archive, "wb") as file:
            file.write(tracker_torrent_url.content)

        # Ready for seeding
        return open(full_path_archive, "rb")

class TransmissionClient(TorrClient):
    def __init__(self) -> None:
        super().__init__()

    def connect(self) -> transmission_rpc:
        try:
            self.client = transmission_rpc.Client(host=config_settings.torrent_client_config.TRASM_HOST,
                                                  port=config_settings.torrent_client_config.TRASM_PORT,
                                                  username=config_settings.torrent_client_config.TRASM_USER,
                                                  password=config_settings.torrent_client_config.TRASM_PASS,
                                                  timeout=10)
            return self.client
        except requests.exceptions.HTTPError:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} HTTP Error. Check IP/port or run Transmission"
            )
        except requests.exceptions.ConnectionError:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} Connection Error. Check IP/port or run Transmission"
            )
        except transmission_rpc.TransmissionError:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} Login required. Check your username and password"
            )
        except Exception as e:
            custom_console.bot_error_log(f"{self.__class__.__name__} Unexpected error: {e}")
            custom_console.bot_error_log(f"{self.__class__.__name__} Please verify your configuration")


    def send_to_client(self,tracker_data_response: str, torrent: Mytorrent, content: Media, archive_path: str):
        # "Translate" files location to shared_path if necessary
        if config_settings.torrent_client_config.SHARED_QBIT_PATH:
            torr_location = config_settings.torrent_client_config.SHARED_QBIT_PATH
        else:
            # If no shared_path is specified set it to the path specified in the CLI commands (path)
            torr_location = os.path.dirname(content.torrent_path)

        # Torrent not created
        if not torrent:
            self.client.add_torrent(
                torrent=open(archive_path, "rb"), download_dir=str(torr_location)
                                    )
        else:
            # Use the new one
            download_torrent_dal_tracker = requests.get(tracker_data_response)
            if download_torrent_dal_tracker.status_code == 200:
                torrent_file = self.download(tracker_torrent_url=download_torrent_dal_tracker,
                                             torrent_path=content.torrent_path)

                self.client.add_torrent(torrent=torrent_file, download_dir=str(torr_location))

    def send_file_to_client(self, torrent_path, archive_path: str ):
        self.client.add_torrent(torrent=open(archive_path, "rb"), download_dir=os.path.dirname(torrent_path))




class QbittorrentClient(TorrClient):
    def __init__(self):
        super().__init__()

    def connect(self) -> qbittorrent:
        try:
            # Requests the protocol type http
            self.client = qbittorrent.Client(f"http://"
                                             f"{config_settings.torrent_client_config.QBIT_HOST}:"
                                             f"{config_settings.torrent_client_config.QBIT_PORT}/",  timeout= 10)

            # return 'None' the login is correct otherwise the login.text error (see client.py python-qbittorrent 0.4.3)
            login_count = 10
            while True:
                login_fail = self.client.login(username=config_settings.torrent_client_config.QBIT_USER,
                                  password=config_settings.torrent_client_config.QBIT_PASS)
                if not login_fail:
                    break
                if login_count > 10:
                    custom_console.bot_error_log("Failed to login.")
                    exit(1)
                custom_console.bot_warning_log("Failed to login. Retry...Please wait")
                time.sleep(2)
                login_count += 1
            return self.client

        except requests.exceptions.HTTPError:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} HTTP Error. Check IP/port or run qBittorrent"
            )

        except requests.exceptions.ConnectionError:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} Connection Error. Check IP/port or run qBittorrent"
            )

        except qbittorrent.client.LoginRequired:
            custom_console.bot_error_log(
                f"{self.__class__.__name__} Login required. Check your username and password"
            )

        except Exception as e:
            custom_console.bot_error_log(f"{self.__class__.__name__} Unexpected error: {e}")
            custom_console.bot_error_log(f"{self.__class__.__name__} Please verify your configuration")


    def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media, archive_path: str):
        # "Translate" files location to shared_path if necessary
        if config_settings.torrent_client_config.SHARED_QBIT_PATH:
            torr_location = config_settings.torrent_client_config.SHARED_QBIT_PATH
        else:
            # If no shared_path is specified set it to the path specified in the CLI commands (path)
            torr_location = os.path.dirname(content.torrent_path)

        # file torrent already created
        if not torrent:
            self.client.download_from_file(
                file_buffer=open(archive_path, "rb"), savepath=str(torr_location)
            )
        else:
            # Use the new one
            download_torrent_dal_tracker = requests.get(tracker_data_response)
            if download_torrent_dal_tracker.status_code == 200:
                torrent_file = self.download(tracker_torrent_url=download_torrent_dal_tracker,
                                             torrent_path=content.torrent_path)

                self.client.download_from_file(file_buffer=torrent_file, savepath=str(torr_location))


    def send_file_to_client(self, torrent_path, archive_path: str):
        self.client.download_from_file(file_buffer=open(archive_path, "rb"),
                                       savepath=os.path.dirname(torrent_path))

