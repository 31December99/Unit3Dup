# -*- coding: utf-8 -*-
import json
import os.path
import requests
from unit3dup import pvtTracker, pvtVideo, pvtTorrent, search, payload, contents
from unit3dup.command import config_tracker
from rich.console import Console

console = Console(log_path=False)


class UploadBot:
    def __init__(self, content: contents):

        self.content = content
        self.file_name = content.file_name  # filename con estensione = filename
        self.folder = content.folder  # folder sia per serie che per movie
        self.tracker_name = content.tracker_name
        self.category = content.category  # 1 = movie , 2 = serie
        self.size = content.size
        self.metainfo = content.metainfo
        self.name = f"{content.name if self.category == 1 else os.path.basename(content.folder)}"

        self.API_TOKEN = config_tracker.instance.api_token
        self.BASE_URL = config_tracker.instance.base_url

    def payload(self, tv_show: search, video: pvtVideo) -> payload:
        return payload.Data.create_instance(metainfo=self.metainfo,
                                            name=self.content.name,
                                            file_name=self.file_name,
                                            result=tv_show,
                                            category=self.content.category,
                                            standard=video.standard,
                                            mediainfo=video.mediainfo,
                                            description=video.description
                                            )

    def send(self, data: payload, torrent: pvtTorrent):
        tracker = pvtTracker.Unit3d(base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key='')
        tracker.data['name'] = data.name
        tracker.data['tmdb'] = data.result.video_id
        tracker.data['keywords'] = data.result.keywords
        tracker.data['category_id'] = data.category
        tracker.data['resolution_id'] = config_tracker.tracker_values.filterResolution(data.file_name)
        tracker.data['sd'] = data.standard
        tracker.data['mediainfo'] = data.media_info
        tracker.data['description'] = data.description
        tracker.data['type_id'] = config_tracker.tracker_values.filterType(data.file_name)
        tracker.data['season_number'] = data.myguess.guessit_season
        tracker.data['episode_number'] = data.myguess.guessit_episode if not self.content.torrent_pack else 0

        # // Send data
        tracker_response = tracker.upload_t(data=tracker.data, file_name=os.path.join(self.content.folder,
                                                                                      str(torrent.torrent_name)))
        # // Seeding
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            console.log(f"\n[TRACKER RESPONSE]............  {tracker_response_body['message'].upper()}")
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                torrent.qbit(download_torrent_dal_tracker)
        else:
            console.log(f"Non è stato possibile fare l'upload => {tracker_response} {tracker_response.text}")
