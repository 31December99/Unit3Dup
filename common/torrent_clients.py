# -*- coding: utf-8 -*-

import os
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
    def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media):
        pass

    def download(self, tracker_torrent_url: requests, torrent_path: str):
        # Archive the torrent file if torrent_archive is set
        if config_settings.user_preferences.TORRENT_ARCHIVE:
            file_name = f"{os.path.basename(torrent_path)}.torrent"
            full_path_archive = os.path.join(config_settings.user_preferences.TORRENT_ARCHIVE, file_name)
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
            custom_console.bot_error_log(f"{self.__class__.__name__} Unexpected error: {str(e)}")
            custom_console.bot_error_log(f"{self.__class__.__name__} Please verify your configuration")


    def send_to_client(self,tracker_data_response: str, torrent: Mytorrent, content: Media):
        full_path_archive = os.path.join(config_settings.user_preferences.TORRENT_ARCHIVE, f"{os.path.basename(content.torrent_path)}.torrent")
        # Torrent not created
        if not torrent:
            self.client.add_torrent(
                torrent=open(full_path_archive, "rb"), download_dir=os.path.dirname(content.torrent_path)
                                    )
        # Use the new one
        else:
            download_torrent_dal_tracker = requests.get(tracker_data_response)
            if download_torrent_dal_tracker.status_code == 200:
                torrent_file = self.download(tracker_torrent_url=download_torrent_dal_tracker,
                                             torrent_path=content.torrent_path)
                self.client.add_torrent(
                    torrent=torrent_file, download_dir=str(torrent.mytorr.location)
                )

    def set_location(self):
        """ Set location for the torrent with shared_path """

        # List of torrents loaded in transmission
        torrents = self.client.get_torrents()

        print(torrents)
        print(config_settings.torrent_client_config.SHARED_PATH)

        for torrent in torrents:
            # Torrent ID
            torrent_id = torrent.id

            # Torrent file location
            save_path = torrent.download_dir
            print(save_path)

            # Torrent status: stalled or seedingf
            state = torrent.status
            print(state)

            # Check if the torrent is stalled or seeding, and the save path doesn't exist
            if (state == 'stalledUP' or state == 'seeding') and not os.path.exists(save_path):
                # If the torrent save path does not exist it is probably stalled
                # Try the shared path instead
                shared_path = config_settings.torrent_client_config.SHARED_PATH
                self.client.move_torrent_data(torrent_id,shared_path)
                custom_console.bot_log(f"Moved torrent data to {shared_path} for {torrent.name} "
                                       f"status: {torrent.status}")


class QbittorrentClient(TorrClient):
    def __init__(self):
        super().__init__()

    def connect(self) -> qbittorrent:
        try:
            # Requests the protocol type http
            self.client = qbittorrent.Client(f"http://"
                                             f"{config_settings.torrent_client_config.QBIT_HOST}:"
                                             f"{config_settings.torrent_client_config.QBIT_PORT}/",  timeout= 10)

            self.client.login(username=config_settings.torrent_client_config.QBIT_USER,
                              password=config_settings.torrent_client_config.QBIT_PASS)
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
        full_path_archive = os.path.join(config_settings.user_preferences.TORRENT_ARCHIVE,
                                         f"{os.path.basename(content.torrent_path)}.torrent")

        # file torrent already created
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


    def set_location(self):
        """ Set location for the torrent with shared_path """

        # List of torrent loaded in qbittorrent

        for torrent in self.client.torrents():

                # Torrent info_hash
                info_hash = torrent['infohash_v1']

                # Torrent file location
                save_path = torrent['save_path']

                # Torrent status:  stalledUP = fail uploading
                state = torrent['state']

                # Stalled wrong path
                if state == 'stalledUP' or state == 'seeding' and not os.path.exists(save_path):
                    # If the torrent save path does not exist it is probably stalled
                    # Try the shared path instead
                    shared_path = config_settings.torrent_client_config.SHARED_PATH
                    self.client.set_torrent_location(info_hash, shared_path)
                    custom_console.bot_log(f"Moved torrent data to {shared_path} for {torrent['name']}"
                                           f" status: {torrent['state']}")



