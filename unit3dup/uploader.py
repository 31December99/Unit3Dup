# -*- coding: utf-8 -*-
import json
import os.path
from unit3dup import pvtTracker, pvtVideo, search, payload, contents
from unit3dup import config
from rich.console import Console

console = Console(log_path=False)


class UploadBot:
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

    def payload(self, tv_show: search, video: pvtVideo) -> payload:
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

    def send(self, tv_show: search, video: pvtVideo):
        # New payload
        data = self.payload(tv_show, video)

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
        tracker.data["mediainfo"] = data.media_info
        tracker.data["description"] = data.description
        tracker.data["type_id"] = self.config.tracker_values.filterType(
            data.file_name
        )
        tracker.data["season_number"] = data.myguess.guessit_season
        tracker.data["episode_number"] = (
            data.myguess.guessit_episode if not self.content.torrent_pack else 0
        )

        # // Send data
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
