import json
import requests

from common.external_services.igdb.core.models.search import Game
from common.trackers.trackers import TRACKData

from unit3dup.pvtTracker import Unit3d
from unit3dup.pvtDocu import PdfImages
from unit3dup import config_settings
from unit3dup.pvtVideo import Video
from unit3dup.media import Media

from view import custom_console

class UploadBot:
    def __init__(self, content: Media, tracker_name: str):

        self.API_TOKEN = config_settings.tracker_config.ITT_APIKEY
        self.BASE_URL = config_settings.tracker_config.ITT_URL
        self.content = content
        self.tracker_name = tracker_name
        self.tracker_data = TRACKData.load_from_module(tracker_name=tracker_name)
        self.tracker = Unit3d(tracker=tracker_name)

    def message(self,tracker_response: requests.Response) -> (requests, dict):

        name_error = ''
        info_hash_error = ''
        _message = json.loads(tracker_response.text)["data"]

        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            custom_console.bot_log(f"\n[RESPONSE]->'{self.tracker_name}'.....{tracker_response_body['message'].upper()}\n\n")
            return tracker_response_body["data"],{}

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

        return {}, error_message

    def send(self,show_id: int , imdb_id: int, show_keywords_list: str, video_info: Video) -> (requests, dict):

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = show_id
        self.tracker.data["imdb"] = imdb_id if imdb_id else 0
        self.tracker.data["keywords"] = show_keywords_list
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["resolution_id"] = self.tracker_data.resolution[self.content.screen_size]\
            if self.content.screen_size else self.tracker_data.resolution[self.content.resolution]
        self.tracker.data["mediainfo"] = video_info.mediainfo
        self.tracker.data["description"] = video_info.description
        self.tracker.data["sd"] = video_info.is_hd
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["season_number"] = self.content.guess_season
        self.tracker.data["episode_number"] = (self.content.guess_episode if not self.content.torrent_pack else 0)
        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path)
        return self.message(tracker_response)

    def send_game(self,igdb: Game, nfo_path = None) -> (requests, dict):

        igdb_platform = self.content.platform_list[0].lower() if self.content.platform_list else ''
        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["description"] = igdb.description if igdb else "Sorry, there is no valid IGDB"
        self.tracker.data["type_id"] = self.tracker_data.type_id.get(igdb_platform) if igdb_platform else 1
        self.tracker.data["igdb"] = igdb.id if igdb else 1,  # need zero not one ( fix tracker)
        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path,
                                               nfo_path=nfo_path)
        return self.message(tracker_response)

    def send_docu(self, document_info: PdfImages):

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["description"] = document_info.description
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["resolution_id"] = ""
        # tracker.data["torrent-cover"] = "" TODO: not yet implemented

        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path)
        return self.message(tracker_response)