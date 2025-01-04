import json
import os
import requests

from common.external_services.igdb.core.models.game import Game
from unit3dup import pvtTracker, payload, contents
from common.trackers.trackers import ITTData
from common.custom_console import custom_console
from abc import ABC, abstractmethod
from common.config import config


class UploadBot(ABC):
    def __init__(self, content: contents):
        self.content = content
        self.file_name = content.file_name
        self.folder = content.folder
        self.tracker_name = content.tracker_name
        self.category = content.category
        self.size = content.size
        self.metainfo = content.metainfo
        self.torrent_path = content.torrent_path
        self.torrent_file_path = os.path.join(self.torrent_path, self.file_name)
        self.API_TOKEN = config.ITT_APIKEY
        self.BASE_URL = config.ITT_URL

    def send(self, tracker: pvtTracker) -> requests:
        tracker_response = tracker.upload_t(
            data=tracker.data, torrent_path=self.torrent_path
        )

        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)

            custom_console.bot_log(
                f"\n[TRACKER RESPONSE]............  {tracker_response_body['message'].upper()}\n\n"
            )
            return tracker_response_body["data"]
        else:
            message = json.loads(tracker_response.text)["data"]
            custom_console.bot_error_log( f"\nIt was not possible to upload the media: "
                                          f"'{message['info_hash'][0].upper()}'\n\n"
            )
        return tracker_response

    @abstractmethod
    def payload(self, **kwargs):
        pass


class UploadDocument(UploadBot):
    def __init__(self, content: contents):
        super().__init__(content)
        self.tracker_data = ITTData.load_from_module()

    def payload(self):
        return payload.Data(
            metainfo=self.metainfo,
            name=self.content.name,
            file_name=self.file_name,
            result="",
            category=self.content.category,
            standard=0,
            media_info="",
            description=self.content.doc_description,
            igdb=0,  # not used
        )

    def tracker(self, data: payload) -> pvtTracker:
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )
        tracker.data["name"] = self.content.display_name
        tracker.data["tmdb"] = 0
        tracker.data["category_id"] = data.category
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.tracker_data.filter_type(data.file_name)
        tracker.data["resolution_id"] = ""
        # tracker.data["torrent-cover"] = "" TODO: not yet implemented
        return tracker


class UploadVideo(UploadBot):
    def __init__(self, content: contents):
        super().__init__(content)
        self.tracker_data = ITTData.load_from_module()

    def payload(self, tv_show: list, video_info: pvtTracker):
        if video_info:
            return payload.Data(
                metainfo=self.metainfo,
                name=self.content.name,
                file_name=self.file_name,
                result=tv_show,
                category=self.content.category,
                media_info=video_info.mediainfo,
                description=video_info.description,
                standard=video_info.is_hd,
                igdb=0,  # not used
            )
        else:
            custom_console.bot_error_log(
                f"[Payload] Unable to create a 'video payload' -> {video_info}"
            )
            return

    def tracker(self, data: payload) -> pvtTracker:
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )
        tracker.data["name"] = self.content.display_name
        tracker.data["tmdb"] = data.result.video_id
        tracker.data["keywords"] = data.result.keywords
        tracker.data["category_id"] = data.category
        tracker.data[
            "resolution_id"] = self.content.screen_size if self.content.screen_size else self.content.resolution
        tracker.data["sd"] = data.standard
        tracker.data["mediainfo"] = data.media_info
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.tracker_data.filter_type(data.file_name)
        tracker.data["season_number"] = data.myguess.guessit_season
        tracker.data["episode_number"] = (
            data.myguess.guessit_episode if not self.content.torrent_pack else 0
        )

        return tracker


class UploadGame(UploadBot):
    def __init__(self, content: contents):
        super().__init__(content)
        self.tracker_data = ITTData.load_from_module()

    def payload(self, igdb: Game):
        return payload.Data(
            metainfo=self.metainfo,
            name=self.content.name,
            file_name=self.file_name,
            result="",
            category=self.content.category,
            standard=0,
            media_info="",
            description=igdb.description,
            igdb=igdb.id,
        )

    def tracker(self, data: payload) -> pvtTracker:
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )
        tracker.data["name"] = self.content.display_name
        tracker.data["tmdb"] = 0
        tracker.data["category_id"] = data.category
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.tracker_data.filter_type(data.file_name)
        tracker.data["resolution_id"] = ""
        tracker.data["igdb"] = data.igdb
        return tracker
