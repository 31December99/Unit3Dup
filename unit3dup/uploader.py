# -*- coding: utf-8 -*-
import json
import os.path
import requests
from decouple import Config, RepositoryEnv
from database.trackers import TrackerConfig
from unit3dup import pvtTracker, pvtVideo, pvtTorrent, userinput, search, payload
from rich.console import Console

console = Console(log_path=False)


class UploadBot:
    def __init__(self, content: userinput):

        self.content = content
        self.file_name = content.file_name  # filename con estensione = filename
        self.folder = content.folder  # folder sia per serie che per movie
        self.tracker_name = content.tracker_name
        self.category = content.category  # 1 = movie , 2 = serie
        self.size = content.size
        self.metainfo = content.metainfo
        self.name = f"{content.name if self.category == 1 else os.path.basename(content.folder)}.torrent"

        # // check tracker file configuration .env e .json
        self.tracker_env = f"{self.tracker_name}.env"
        config_load = Config(RepositoryEnv(self.tracker_env))
        self.PASS_KEY = config_load('PASS_KEY')
        self.API_TOKEN = config_load('API_TOKEN')
        self.BASE_URL = config_load('BASE_URL')

        if not self.PASS_KEY or not self.API_TOKEN:
            console.log("il file .env non è stato configurato oppure i nomi delle variabili sono errate.")
            return

        self.tracker_json = f"{self.tracker_name}.json"
        self.tracker_values = TrackerConfig(self.tracker_json)
        console.log(f"\n[TRACKER {self.tracker_name.upper()}]..............  {self.BASE_URL}")

    def serie_data(self) -> payload:
        mytmdb = search.TvShow('Serie')
        video = pvtVideo.Video(fileName=str(os.path.join(self.folder, self.file_name)))
        return payload.Data.create_instance(metainfo=self.metainfo,
                                            name=os.path.basename(self.folder),
                                            file_name=self.file_name,
                                            result=mytmdb.start(self.file_name),
                                            category=self.tracker_values.category('tvshow'),
                                            standard=video.standard,
                                            mediainfo=video.mediainfo,
                                            description=video.description,
                                            freelech=self.tracker_values.get_freelech(video.size))

    def movie_data(self) -> payload:
        mytmdb = search.TvShow('Movie')
        video = pvtVideo.Video(fileName=str(os.path.join(self.folder, self.file_name)))
        return payload.Data.create_instance(metainfo=self.metainfo,
                                            name=self.name,
                                            file_name=self.file_name,
                                            result=mytmdb.start(self.file_name),
                                            category=self.tracker_values.category('movie'),
                                            standard=video.standard,
                                            mediainfo=video.mediainfo,
                                            description=video.description,
                                            freelech=self.tracker_values.get_freelech(video.size))

    def process_data(self, data: payload):

        tracker = pvtTracker.Unit3d(base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY)
        tracker.data['name'] = data.name
        tracker.data['tmdb'] = data.result.video_id
        tracker.data['keywords'] = data.result.keywords
        tracker.data['category_id'] = data.category
        tracker.data['resolution_id'] = self.tracker_values.filterResolution(data.file_name)
        tracker.data['free'] = data.freelech
        tracker.data['sd'] = data.standard
        tracker.data['mediainfo'] = data.media_info
        tracker.data['description'] = data.description
        tracker.data['type_id'] = self.tracker_values.filterType(data.file_name)
        tracker.data['season_number'] = data.myguess.guessit_season
        tracker.data['episode_number'] = data.myguess.guessit_season

        # // Torrent
        mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.content.metainfo,
                                         tracker_announce_list=[f"{self.BASE_URL}/announce/{self.PASS_KEY}/"])
        mytorrent.write()

        # // Send data
        tracker_response = tracker.upload_t(data=tracker.data, file_name=os.path.join(self.content.folder,
                                                                                      mytorrent.torrent_name))
        # // Seeding
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            console.log(f"\n[TRACKER RESPONSE]............  {tracker_response_body['message'].upper()}")
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                mytorrent.qbit(download_torrent_dal_tracker)
        else:
            console.log(f"Non è stato possibile fare l'upload => {tracker_response} {tracker_response.text}")
