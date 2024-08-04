import json
import os

import requests

from unit3dup import pvtTracker, payload, contents
from abc import ABC, abstractmethod
from unit3dup import config
from rich.console import Console

console = Console(log_path=False)


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

        self.config = config.trackers.get_tracker(self.tracker_name)
        self.API_TOKEN = self.config.api_token
        self.BASE_URL = self.config.base_url

    def send(self, tracker: pvtTracker) -> requests:
        tracker_response = tracker.upload_t(
            data=tracker.data, file_name=self.torrent_path
        )
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            console.log(
                f"\n[TRACKER RESPONSE]............  {tracker_response_body['message'].upper()}"
            )
            return tracker_response_body["data"]
        else:
            console.log(
                f"It was not possible to upload => {tracker_response} {tracker_response.text}"
            )
        return tracker_response

    @abstractmethod
    def payload(self, **kwargs):
        pass


class UploadDocument(UploadBot):
    def __init__(self, content: contents):
        super().__init__(content)

    def payload(self, **kwargs):
        return payload.Data.create_instance(
            metainfo=self.metainfo,
            name=self.content.name,
            file_name=self.file_name,
            result="",
            category=self.content.category,
            standard=0,
            mediainfo="",
            description=self.content.doc_description,
        )

    def tracker(self, data: payload) -> pvtTracker:
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )
        tracker.data["name"] = self.content.display_name
        tracker.data["tmdb"] = 0
        tracker.data["category_id"] = data.category
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.config.tracker_values.filterType(data.file_name)
        return tracker


class UploadVideo(UploadBot):
    def __init__(self, content: contents):
        super().__init__(content)

    def payload(self, **kwargs):
        tv_show = kwargs.get("tvshow", None)
        video = kwargs.get("video", None)

        if video:
            return payload.Data.create_instance(
                metainfo=self.metainfo,
                name=self.content.name,
                file_name=self.file_name,
                result=tv_show,
                category=self.content.category,
                standard=video.standard,
                mediainfo=video.mediainfo,
                description=video.description,
            )
        else:
            console.log(f"[Payload] Unable to create a 'video payload' -> {video}")
            return

    def tracker(self, data: payload) -> pvtTracker:
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )
        tracker.data["name"] = self.content.display_name
        tracker.data["tmdb"] = data.result.video_id
        tracker.data["keywords"] = data.result.keywords
        tracker.data["category_id"] = data.category
        tracker.data["resolution_id"] = self.config.tracker_values.filterResolution(
            data.file_name
        )
        tracker.data["sd"] = data.standard
        tracker.data["mediainfo"] = data.mediainfo
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.config.tracker_values.filterType(data.file_name)
        tracker.data["season_number"] = data.myguess.guessit_season
        tracker.data["episode_number"] = (
            data.myguess.guessit_episode if not self.content.torrent_pack else 0
        )

        return tracker
