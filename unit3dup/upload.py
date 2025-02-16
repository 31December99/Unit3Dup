import json
import requests

from common.external_services.igdb.core.models.search import Game
from common.custom_console import custom_console
from common.trackers.trackers import ITTData

from unit3dup.pvtTracker import Unit3d
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
from unit3dup import config

class UploadBot:
    def __init__(self, content: Media):

        self.API_TOKEN = config.ITT_APIKEY
        self.BASE_URL = config.ITT_URL
        self.content = content
        self.tracker_data = ITTData.load_from_module()
        self.tracker = Unit3d(base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key="")

    @staticmethod
    def message(tracker_response: requests.Response) -> (requests, dict):

        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            custom_console.bot_log(f"\n[TRACKER RESPONSE]............  {tracker_response_body['message'].upper()}\n\n")
            custom_console.rule()
            return tracker_response_body["data"],{}
        else:
            error_message = json.loads(tracker_response.text)["data"]
        custom_console.rule()
        return {}, error_message

    def send(self,show_id: int , show_keywords_list: str, video_info: Video) -> (requests, dict):

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = show_id
        self.tracker.data["keywords"] = show_keywords_list
        self.tracker.data["category_id"] = self.content.category
        self.tracker.data[
            "resolution_id"] = self.content.screen_size if self.content.screen_size else self.content.resolution
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
        self.tracker.data["category_id"] = self.content.category
        self.tracker.data["description"] = igdb.description if igdb else "Sorry, there is no valid IGDB"
        self.tracker.data["type_id"] = self.tracker_data.type_id.get(igdb_platform)
        self.tracker.data["igdb"] = igdb.id if igdb else 1,  # need zero not one ( fix tracker)

        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path,
                                               nfo_path=nfo_path)
        return self.message(tracker_response)

    def send_docu(self):

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.content.category
        self.tracker.data["description"] = self.content.doc_description
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["resolution_id"] = ""
        # tracker.data["torrent-cover"] = "" TODO: not yet implemented

        tracker_response=self.tracker.upload_t(data=self.tracker.data, torrent_path=self.content.torrent_path)
        return self.message(tracker_response)