# -*- coding: utf-8 -*-
import hashlib
import os
import time
import bencode2
import requests
from abc import ABC, abstractmethod

import qbittorrent
import transmission_rpc
from rtorrent_rpc import RTorrent
from qbittorrent import Client as QBClient

from unit3dup.pvtTorrent import Mytorrent
from unit3dup import config_settings
from unit3dup.media import Media

from view import custom_console

class MyQbittorrent(QBClient):
    """
    Extends qbittorrent import
    """
    def add_tags(self, infohash_list: list):

        return self._post('torrents/addTags', data={
            'hashes': infohash_list[0],
            'tags': config_settings.torrent_client_config.TAG,
        })

    def remove_tags(self, infohash_list: list):
        return self._post('torrents/removeTags', data={
            'hashes': infohash_list[0],
            'tags': config_settings.torrent_client_config.TAG
        })

class TorrClient(ABC):

    def __init__(self):
        self.client = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media, archive_path: str):
        pass

    @staticmethod
    def download(tracker_torrent_url: requests, full_path_archive: str):
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

        # Send to the client
        with open(archive_path, "rb") as file_buffer:
            self.client.add_torrent(torrent=file_buffer, download_dir=str(torr_location))


    def send_file_to_client(self, torrent_path: str):
        self.client.add_torrent(torrent=open(torrent_path, "rb"), download_dir=str(os.path.dirname(torrent_path)))



class QbittorrentClient(TorrClient):
    def __init__(self):
        super().__init__()


    def connect(self) -> MyQbittorrent | None:
        try:
            # Requests the protocol type http
            self.client = MyQbittorrent(f"http://"
                                             f"{config_settings.torrent_client_config.QBIT_HOST}:"
                                             f"{config_settings.torrent_client_config.QBIT_PORT}/",  timeout= 10)

            # return 'None' the login is correct otherwise the login.text error (see client.py python-qbittorrent 0.4.3)
            login_count = 0
            while True:
                login_fail = self.client.login(username=config_settings.torrent_client_config.QBIT_USER,
                                  password=config_settings.torrent_client_config.QBIT_PASS)
                if not login_fail:
                    break
                if login_count > 5:
                    custom_console.bot_error_log("Failed to login.")
                    exit(1)
                custom_console.bot_warning_log("Qbittorrent failed to login. Retry...Please wait")
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
            with open(archive_path, "rb") as file_buffer:
                # Get the info_hash
                torrent_data = file_buffer.read()
                info = bencode2.bdecode(torrent_data)[b'info']
                info_hash = hashlib.sha1(bencode2.bencode(info)).hexdigest()
                # rewind !
                file_buffer.seek(0)
                # Send to the client
                self.client.download_from_file(file_buffer=file_buffer, savepath=str(torr_location))
                # Set the TAG in qbittorrent
                self.client.add_tags([info_hash])
        else:
            # Use the new one
            # Get the info_hash from the torf instance
            info = torrent.mytorr.metainfo['info']
            info_hash = hashlib.sha1(bencode2.bencode(info)).hexdigest()

            # Read and send
            with open(archive_path, "rb") as file_buffer:
                self.client.download_from_file(file_buffer=file_buffer, savepath=str(torr_location))

            # Set the TAG in qbittorrent
            self.client.add_tags([info_hash])


    def send_file_to_client(self, torrent_path: str, media_location: str):
        self.client.download_from_file(file_buffer=open(torrent_path, "rb"), savepath=media_location)


class RTorrentClient(TorrClient):
        def __init__(self):
            super().__init__()

        def connect(self) -> RTorrent | None:

            login_count = 0
            while True:
                try:
                    self.client = RTorrent(address=f"scgi://"
                                                 f"{config_settings.torrent_client_config.RTORR_HOST}:"
                                                 f"{config_settings.torrent_client_config.RTORR_PORT}",  timeout= 10)
                    # Test
                    self.client.system_list_methods()
                    return self.client
                except requests.exceptions.HTTPError:
                    custom_console.bot_warning_log("Rtorrent failed to login. Retry...Please wait")
                    time.sleep(2)
                    login_count += 1
                    if login_count > 5:
                        custom_console.bot_error_log("Rtorrent failed to login.")
                        exit()
                except requests.exceptions.ConnectionError:
                    custom_console.bot_error_log(
                        f"{self.__class__.__name__} Connection Error. Check IP/port or run rTorrent"
                    )
                    exit()

                except TimeoutError:
                    custom_console.bot_error_log(
                        f"{self.__class__.__name__} Connection Error. Check IP/port or run rTorrent"
                    )
                    exit()

        def send_to_client(self, tracker_data_response: str, torrent: Mytorrent, content: Media, archive_path: str):
            # "Translate" files location to shared_path if necessary
            if config_settings.torrent_client_config.SHARED_RTORR_PATH:
                torr_location = config_settings.torrent_client_config.SHARED_RTORR_PATH
            else:
                # If no shared_path is specified set it to the path specified in the CLI commands (path)
                torr_location = os.path.dirname(content.torrent_path)

            # Add the torrent folder needed for rTorrent
            if os.path.isdir(content.folder):
                torr_location =  os.path.join(torr_location, content.torrent_name)
                # Save path for Windows or Linux.The root directory (/mnt or c:\) is the responsibility of the user
                # in shared_folder
                torr_location = torr_location.replace('\\', '/')

            # Read and send
            with open(archive_path, "rb") as file:
                self.client.add_torrent_by_file(content=file.read(), directory_base=str(torr_location),
                                                tags=[config_settings.torrent_client_config.TAG])



        def send_file_to_client(self, torrent_path: str, media_location: str):
            with open(torrent_path, "rb") as file:
                self.client.add_torrent_by_file(content=file.read(), directory_base=str(media_location),
                                                tags=[config_settings.torrent_client_config.TAG])

