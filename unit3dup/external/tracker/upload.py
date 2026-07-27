import pprint
import requests
import json

from unit3dup.external.igdb.core.models.search import Game
from unit3dup.external.tracker.trackers import TRACKData
from unit3dup.external.document.pvtDocu import PdfImages
from unit3dup.external.tracker.pvtTracker import Unit3d
from unit3dup.external.media import Media

from unit3dup.config.bot_config import BotConfig
from unit3dup.view import custom_console

from unit3dup.config.settings import Load

config_settings = Load().config


class UploadBot:
    def __init__(self, content: Media, tracker_name: str, cli: BotConfig):
        self.cli = cli
        self.content = content
        self.tracker_name = tracker_name
        self.tracker_data = TRACKData.load_from_module(tracker_name=tracker_name)
        self.tracker = Unit3d(tracker_name=tracker_name)
        self.sign = (
            "[url=https://github.com/31December99/Unit3Dup]"
            "[code][color=#00BFFF][size=14]"
            f"Uploaded with Unit3Dup {Load.version}"
            "[/size][/color][/code][/url]"
        )

    def message(self, tracker_response: requests.Response):

        name_error = ''
        info_hash_error = ''
        _message = json.loads(tracker_response.text)
        if 'data' in _message:
            _message = _message['data']

        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            custom_console.bot_log(
                f"\n[RESPONSE]-> '{self.tracker_name}'.....{tracker_response_body['message'].upper()}\n\n")
            custom_console.rule()
            return tracker_response_body["data"], {}

        elif tracker_response.status_code == 401:
            custom_console.bot_error_log(_message)
            exit(_message['message'])

        elif tracker_response.status_code == 403:
            custom_console.bot_error_log(f"{self.__class__.__name__} HTTP 403 Upload right disabled\n")
            custom_console.bot_error_log(self.content.file_name)

        elif tracker_response.status_code == 404:
            error_message = f"{self.__class__.__name__} - {_message}"

        elif tracker_response.status_code == 500:
            custom_console.bot_error_log(f"{self.__class__.__name__} HTTP 500 Internal Tracker Error\n")
            pprint.pprint(self.tracker.data)
            custom_console.bot_error_log(self.content.file_name)
            exit()

        else:
            if _message.get("name", None):
                name_error = _message["name"][0]
            if _message.get("info_hash", None):
                info_hash_error = _message["info_hash"][0]
            error_message = f"{self.__class__.__name__} - {name_error} : {info_hash_error}"

        custom_console.bot_error_log(f"\n[RESPONSE]-> '{error_message}\n\n")
        custom_console.rule()
        return {}, error_message

    def resolution_id(self) -> int | None:
        value = self.content.resolution
        _id = self.tracker_data.resolution.get(value)
        if not _id:
            custom_console.bot_error_log(f"Resolution ID {value} not found")
        return _id

    def category_id(self) -> int | None:
        _id = self.tracker_data.category.get(self.content.category)
        if not _id:
            custom_console.bot_error_log(f"Category ID {self.content.category} not found")
        return _id

    def data(self, content: Media) -> Unit3d | None:

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = content.media_result.video_id
        self.tracker.data["imdb"] = content.media_result.imdb_id if content.media_result.imdb_id else 0
        self.tracker.data[
            "tvdb"] = content.media_result.tvdb_id if content.media_result.tvdb_id and self.content.category == 'tv' else None
        self.tracker.data["keywords"] = content.media_result.keywords_list
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["mediainfo"] = content.mediafile.info
        self.tracker.data["description"] = content.torrent_description + self.sign
        self.tracker.data["sd"] = content.is_hd
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["season_number"] = self.content.guess_season
        self.tracker.data["episode_number"] = (self.content.guess_episode if not self.content.torrent_pack else 0)
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                 or int(self.cli.personal))
        self.tracker.data["internal"] = int(self.cli.internal)
        self.tracker.data["mod_queue_opt_in"] = int(self.cli.moderation)

        # skip upload if the key is missing
        category_id = self.category_id()
        if category_id:
            self.tracker.data["category_id"] = category_id
        else:
            return None

        resolution_id = self.resolution_id()
        if resolution_id:
            self.tracker.data["resolution_id"] = resolution_id
        else:
            return None

        return self.tracker

    def data_game(self, igdb: Game) -> Unit3d | None:

        igdb_platform = self.content.platform_list[0].lower() if self.content.platform_list else ''
        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["description"] = igdb.description + self.sign if igdb else "Sorry, there is no valid IGDB"
        self.tracker.data["type_id"] = self.tracker_data.type_id.get(igdb_platform) if igdb_platform else 1
        self.tracker.data["igdb"] = igdb.id if igdb else 1  # need zero not one ( fix tracker)
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                 or int(self.cli.personal))
        return self.tracker

    def data_docu(self, document_info: PdfImages) -> Unit3d | None:

        self.tracker.data["name"] = self.content.display_name
        self.tracker.data["tmdb"] = 0
        self.tracker.data["category_id"] = self.tracker_data.category.get(self.content.category)
        self.tracker.data["anonymous"] = int(config_settings.user_preferences.ANON)
        self.tracker.data["description"] = document_info.description + self.sign
        self.tracker.data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        self.tracker.data["resolution_id"] = ""
        self.tracker.data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                 or int(self.cli.personal))
        return self.tracker

    def send(self, nfo_path=None):

        tracker_response = self.tracker.upload_t(data=self.tracker.data,
                                                 torrent_archive_path=self.content.torrent_metadata_path,
                                                 nfo_path=nfo_path)

        return self.message(tracker_response=tracker_response)
