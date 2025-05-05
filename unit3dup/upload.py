import json
import requests

from common.trackers.trackers import TRACKData
from common.bittorrent import BittorrentData

from unit3dup.pvtTracker import Unit3d
from unit3dup import config_settings, Load

from abc import ABC, abstractmethod
from view import custom_console


class UploadBot(ABC):
    def __init__(self, torrent: BittorrentData):

        self.API_TOKEN = config_settings.tracker_config.ITT_APIKEY
        self.BASE_URL = config_settings.tracker_config.ITT_URL
        self.torrent = torrent
        self.cli = torrent.payload.cli
        self.content = torrent.content
        self.tracker_name = torrent.payload.tracker_name
        self.tracker_data = TRACKData.load_from_module(tracker_name=torrent.payload.tracker_name)
        self.tracker = Unit3d(tracker_name=torrent.payload.tracker_name)
        self.sign = (f"[url=https://github.com/31December99/Unit3Dup][code][color=#00BFFF][size=14]Uploaded with Unit3Dup"
                     f" {Load.version}[/size][/color][/code][/url]")

    def message(self,tracker_response: requests.Response) -> (requests, dict):

        name_error = ''
        info_hash_error = ''
        _message = json.loads(tracker_response.text)
        if 'data' in _message:
            _message = _message['data']

        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            custom_console.bot_log(f"\n[RESPONSE]-> '{self.tracker_name}'.....{self.torrent.content.display_name} "
                                   f"{tracker_response_body['message'].upper()}\n")
            return tracker_response_body["data"],{}

        elif tracker_response.status_code == 401:
            custom_console.bot_error_log(_message)
            exit(_message['message'])

        elif tracker_response.status_code == 404:
            if _message.get("type_id",None):
                name_error =  _message["type_id"]
            else:
                name_error = _message
            error_message = f"{self.__class__.__name__} - {name_error}"
        else:
            if _message.get("name",None):
                name_error =  _message["name"][0]
            if _message.get("info_hash",None):
                info_hash_error = _message["info_hash"][0]
            error_message =f"{self.__class__.__name__} - {name_error} : {info_hash_error}"

        custom_console.bot_error_log(f"\n[RESPONSE]-> '{error_message}\n\n")
        custom_console.rule()
        return {}, error_message

    def _send(self, torrent_archive: str, nfo_path = None) -> (requests, dict):
        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path,
                                        torrent_archive_path = torrent_archive,nfo_path=nfo_path)
        return self.message(tracker_response)


    @abstractmethod
    def send(self, torrent_archive: str, nfo_path = None) -> (requests, dict):
        pass


class Show(UploadBot):
    def send(self, path: str, nfo_path = None) -> (requests, dict):
        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = self.torrent.payload.show_id
        self.tracker.data["imdb"] = self.torrent.payload.imdb_id if self.torrent.payload.imdb_id else 0
        self.tracker.data["keywords"] = self.torrent.payload.show_keywords
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["resolution_id"] = self.tracker_data.resolution[self.content.screen_size] \
            if self.content.screen_size else self.tracker_data.resolution[self.content.resolution]
        self.tracker.data["mediainfo"] = self.torrent.payload.video_info.mediainfo
        self.tracker.data["description"] = self.torrent.payload.video_info.description + self.sign
        self.tracker.data["sd"] = self.torrent.payload.video_info.is_hd
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["season_number"] = self.content.guess_season
        self.tracker.data["episode_number"] = (self.content.guess_episode if not self.content.torrent_pack else 0)
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                 or int(self.cli.personal))
        return self._send(torrent_archive=path)


class Games(UploadBot):
    def send(self, path: str, nfo_path=None) -> (requests, dict):
        igdb_platform = self.content.platform_list[0].lower() if self.content.platform_list else ''
        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["description"] = self.torrent.payload.igdb.description + self.sign if self.torrent.payload.igdb else "Sorry, there is no valid IGDB"
        self.tracker.data["type_id"] = self.tracker_data.type_id.get(igdb_platform) if igdb_platform else 1
        self.tracker.data["igdb"] = self.torrent.payload.igdb.id if self.torrent.payload.igdb else 1,  # need zero not one ( fix tracker)
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                             or int(self.cli.personal))
        return self._send(torrent_archive=path, nfo_path=nfo_path)


class Doc(UploadBot):
    def send(self, path: str, nfo_path=None) -> (requests, dict):
        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["description"] = self.torrent.payload.docu_info.description + self.sign
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["resolution_id"] = ""
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                     or int(self.cli.personal))
        return self._send(torrent_archive=path)