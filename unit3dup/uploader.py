# -*- coding: utf-8 -*-
import json
import os
import requests
from decouple import Config, RepositoryEnv
from database.trackers import TrackerConfig
from unit3dup import pvtTracker, pvtVideo, pvtTorrent, userinput, search, payload
from rich.console import Console

console = Console(log_path=False)


class UploadBot:
    def __init__(self, content: userinput):
        self.content = content
        self.file_name = content.file_name
        self.folder = content.folder
        self.tracker_name = content.tracker_name
        self.category = content.category
        self.size = content.size
        self.metainfo = content.metainfo
        self.name = self._get_name()

        self._load_tracker_config()

    def _get_name(self):
        if self.category == 1:
            return self.content.name
        return os.path.basename(self.folder)

    def _load_tracker_config(self):
        self.tracker_env = f"{self.tracker_name}.env"
        config_load = Config(RepositoryEnv(self.tracker_env))
        self.PASS_KEY = config_load('PASS_KEY')
        self.API_TOKEN = config_load('API_TOKEN')
        self.BASE_URL = config_load('BASE_URL')

        if not self.PASS_KEY or not self.API_TOKEN:
            console.log("Configuration file '.env' is missing or variables are incorrect.")
            raise ValueError("Invalid configuration in .env file.")

        self.tracker_json = f"{self.tracker_name}.json"
        self.tracker_values = TrackerConfig(self.tracker_json)
        console.log(f"\n[TRACKER {self.tracker_name.upper()}]..............  {self.BASE_URL}")

    def _create_payload(self, name: str) -> payload:
        mytmdb = search.TvShow('Serie' if self.category == 2 else 'Movie')
        video = pvtVideo.Video(fileName=str(os.path.join(self.folder, self.file_name)))
        return payload.Data.create_instance(
            metainfo=self.metainfo,
            name=name,
            file_name=self.file_name,
            result=mytmdb.start(self.file_name),
            category=self.tracker_values.category('tvshow' if self.category == 2 else 'movie'),
            standard=video.standard,
            mediainfo=video.mediainfo,
            description=video.description,
            freelech=self.tracker_values.get_freelech(video.size)
        )

    def serie_data(self) -> payload:
        return self._create_payload(os.path.basename(self.folder))

    def movie_data(self) -> payload:
        return self._create_payload(self.name)

    def process_data(self, data: payload):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL,
            api_token=self.API_TOKEN,
            pass_key=self.PASS_KEY
        )
        self._set_tracker_data(tracker, data)
        self._send(tracker, data)

    def _set_tracker_data(self, tracker, data: payload):
        tracker.data.update({
            'name': data.name,
            'tmdb': data.result.video_id,
            'keywords': data.result.keywords,
            'category_id': data.category,
            'resolution_id': self.tracker_values.filterResolution(data.file_name),
            'free': data.freelech,
            'sd': data.standard,
            'mediainfo': data.media_info,
            'description': data.description,
            'type_id': self.tracker_values.filterType(data.file_name),
            'season_number': data.myguess.guessit_season,
            'episode_number': data.myguess.guessit_season
        })

    def _send(self, tracker, data: payload):
        mytorrent = pvtTorrent.Mytorrent(
            contents=self.content,
            meta=self.content.metainfo,
            tracker_announce_list=[f"{self.BASE_URL}/announce/{self.PASS_KEY}/"]
        )
        mytorrent.write()

        """
        tracker_response = tracker.upload_t(
            data=tracker.data,
            file_name=os.path.join(self.content.folder, mytorrent.torrent_name)
        )

        if tracker_response.status_code == 200:
            self._send_to_qbitt(tracker_response)
        else:
            console.log(f"Upload failed => {tracker_response} {tracker_response.text}")
        """

    def _send_to_qbitt(self, response):
        response_body = json.loads(response.text)
        console.log(f"\n[TRACKER RESPONSE]............  {response_body['message'].upper()}")
        torrent_url = response_body.get('data')

        if torrent_url:
            download_response = requests.get(torrent_url)
            if download_response.status_code == 200:
                pvtTorrent.Mytorrent.qbit(self.content, download_response)
            else:
                console.log(f"Failed to download torrent => {download_response}")
        else:
            console.log("No torrent URL provided in response.")
