# -*- coding: utf-8 -*-

import os
import requests
import qbittorrent
import transmission_rpc
from abc import ABC, abstractmethod

from common.custom_console import custom_console
from unit3dup.media import Media
from unit3dup.pvtTorrent import Mytorrent
from unit3dup import config

class TorrClient(ABC):

    def __init__(self):
        self.client = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media):
        pass

    def download(self, tracker_torrent_url: requests, torrent_path: str):
        # Archive the torrent file if torrent_archive is set
        if config.user_preferences.TORRENT_ARCHIVE:
            file_name = f"{os.path.basename(torrent_path)}.torrent"
            full_path_archive = os.path.join(config.user_preferences.TORRENT_ARCHIVE, file_name)
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
            self.client = transmission_rpc.Client(host=config.torrent_client_config.TRASM_HOST,
                                                  port=config.torrent_client_config.TRASM_PORT,
                                                  username=config.torrent_client_config.TRASM_USER,
                                                  password=config.torrent_client_config.TRASM_PASS,
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
            custom_console.bot_error_log(f"{self.__class__.__name__} Unexpected error: {str(e)}")
            custom_console.bot_error_log(f"{self.__class__.__name__} Please verify your configuration")


    def send_to_client(self,tracker_data_response: str, torrent: Mytorrent, content: Media):
        full_path_archive = os.path.join(config.user_preferences.TORRENT_ARCHIVE, f"{os.path.basename(content.torrent_path)}.torrent")
        if not torrent:
            self.client.add_torrent(
                torrent=open(full_path_archive, "rb"), download_dir=os.path.dirname(content.torrent_path)
                                    )
        else:
            # Use the new one
            download_torrent_dal_tracker = requests.get(tracker_data_response)
            if download_torrent_dal_tracker.status_code == 200:
                torrent_file = self.download(tracker_torrent_url=download_torrent_dal_tracker,
                                             torrent_path=content.torrent_path)
                self.client.add_torrent(
                    torrent=torrent_file, download_dir=torrent.mytorr.location
                )


class QbittorrentClient(TorrClient):
    def __init__(self):
        super().__init__()

    def connect(self) -> qbittorrent:
        try:
            # Requests the protocol type http
            self.client = qbittorrent.Client(f"http://"
                                             f"{config.torrent_client_config.QBIT_HOST}:"
                                             f"{config.torrent_client_config.QBIT_PORT}/",  timeout= 10)

            self.client.login(username=config.torrent_client_config.QBIT_USER,
                              password=config.torrent_client_config.QBIT_PASS)
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
            custom_console.bot_error_log(f"{self.__class__.__name__} Unexpected error: {str(e)}")


    def send_to_client(self,tracker_data_response: str, torrent: Mytorrent, content: Media):
        full_path_archive = os.path.join(config.user_preferences.TORRENT_ARCHIVE, f"{os.path.basename(content.torrent_path)}.torrent")
        if not torrent:
            self.client.download_from_file(
                file_buffer=open(full_path_archive, "rb"), savepath=os.path.dirname(content.torrent_path)
            )
        else:
            # Use the new one
            download_torrent_dal_tracker = requests.get(tracker_data_response)
            if download_torrent_dal_tracker.status_code == 200:
                torrent_file = self.download(tracker_torrent_url=download_torrent_dal_tracker,
                                             torrent_path=content.torrent_path)
                self.client.download_from_file(
                    file_buffer=torrent_file, savepath=torrent.mytorr.location
                )
