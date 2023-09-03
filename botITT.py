#!/usr/bin/env python3.9
import argparse
import os.path
import requests
import pvtTracker
import myTMDB
import pvtVideo
import pvtTorrent
import utitlity
import Contents
from decouple import config

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')


class ITtorrents:

    def __init__(self):

        if not ITT_PASS_KEY or not ITT_API_TOKEN:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        self.Itt = pvtTracker.ITT(base_url="https://itatorrents.xyz/", api_token=ITT_API_TOKEN,
                                  pass_key=ITT_PASS_KEY)

        parser = argparse.ArgumentParser(description='Commands', add_help=False)
        parser.add_argument('-serie', '--serie', nargs=1, type=str, help='FileName')
        parser.add_argument('-file', '--file', nargs=1, type=str, help='FileName')
        args = parser.parse_args()
        if args.serie:
            self.content = Contents.Args(args.serie)
            metainfo = self.content.folder()
            self.myguess = myTMDB.Myguessit(self.content.base_name)
            self.Itt.data['type_id'] = utitlity.Manage_titles.filterType(self.content.base_name)
            self.Itt.data['name'] = self.content.base_name
            self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=metainfo)

        if args.file:
            self.content = Contents.Args(args.file)
            metainfo = self.content.file()
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.Itt.data['type_id'] = utitlity.Manage_titles.filterType(self.content.file_name)
            self.Itt.data['name'] = self.content.tracker_file_name
            self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=metainfo)

        self.video = pvtVideo.Video(fileName=os.path.join(self.content.path, self.content.file_name))
        self.torrent = self.mytorrent.write
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.video.freeLech
        self.Itt.data['free'] = self.freelech
        self.Itt.data['sd'] = self.standard
        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = self.descrizione

        if 'movie' in self.myguess.type:
            self.Itt.data['category_id'] = 1
            self.tmdb_movie = myTMDB.TmdbMovie(self.myguess)
            self.video_id = self.tmdb_movie.cerca()

        else:
            self.tmdb_series = myTMDB.TmdbSeries(self.myguess)
            self.video_id = self.tmdb_series.cerca()
            self.Itt.data['category_id'] = 2
            self.Itt.data['season_number'] = self.myguess.guessit_season
            self.Itt.data['episode_number'] = self.myguess.guessit_episode

        tracker_response = self.Itt.upload_t(data=self.Itt.data,
                                             video_id=self.video_id,
                                             file_name=os.path.join(self.content.path,
                                                                    self.mytorrent.read()))  # self.video.file_name)
        upload_success = tracker_response['success']

        if upload_success:
            link_torrent_dal_tracker = tracker_response['data']
            messaggio_dal_tracker = tracker_response['message']
            pvtTracker.Utility.console(upload_success, 2)
            pvtTracker.Utility.console(link_torrent_dal_tracker, 2)
            pvtTracker.Utility.console(messaggio_dal_tracker, 2)

            download_torrent_dal_tracker = requests.get(link_torrent_dal_tracker)
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)

        else:
            pvtTracker.Utility.console(f"Non è stato possibile fare l'upload => {tracker_response}", 1)


if os.name == 'nt':
    os.system('color')

ittorrents = ITtorrents()
