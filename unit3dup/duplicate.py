# -*- coding: utf-8 -*-

from unit3dup.torrent import Torrent
from unit3dup.contents import Contents
from rich.console import Console
from unit3dup import title
from unit3dup.search import TvShow
from unit3dup import config

console = Console(log_path=False)


class Series:
    """
     compare available episodes with local file
    """

    def __init__(self, raw_data: dict, season: int, episode: int):
        # Tracker data from searching tmdb id
        self.raw_data = raw_data
        self.season = season
        self.episode = episode

    def video(self) -> bool:
        for data in self.raw_data['data']:
            file_name = data['attributes']['files'][0]['name']
            guess_filename = title.Guessit(file_name)
            season = guess_filename.guessit_season
            episode = guess_filename.guessit_episode
            if self.season == season and self.episode == episode:
                return True
        return False


class Movies:
    """
     compare available movie title with local file
    """

    def __init__(self, raw_data: dict, name: str):
        # Tracker data from searching tmdb id
        self.raw_data = raw_data
        self.name = name

    def video(self) -> bool:
        # Compare title content vs title found on tracker
        for data in self.raw_data['data']:
            file_name = data['attributes']['files'][0]['name']
            guess_filename_tracker = title.Guessit(file_name).guessit_title
            guess_filename_content = title.Guessit(self.name).guessit_title
            if guess_filename_content.lower() == guess_filename_tracker.lower():
                return True
        return False


class Duplicate:

    def __init__(self, content: Contents):
        self.content: Contents = content
        self.torrent_info = Torrent()
        self.config = config.trackers.get_tracker(tracker_name=content.tracker_name)
        self.movie_category = self.config.tracker_values.category("movie")
        self.serie_category = self.config.tracker_values.category("tvshow")
        self.guess_filename = title.Guessit(self.content.name)

    def search_by_tmdb(self, tmdb_id: int) -> bool:
        """
         Search media by tmdb id on the tracker

        """
        # Request results from the video online database
        # Get Season
        season = self.guess_filename.guessit_season

        # Get episode
        episode = self.guess_filename.guessit_episode

        # Search for local files in tmdb
        my_tmdb = TvShow(self.content.category)

        # Get Result
        tv_show_result = my_tmdb.start(self.content.file_name)

        # Request to tracker max 25 item result
        raw_data = self.torrent_info.get_by_tmdb_id(tmdb_id=tmdb_id)

        if self.content.category == self.serie_category:
            series = Series(raw_data=raw_data, season=season, episode=episode)
            return series.video()

        if self.content.category == self.movie_category:
            movies = Movies(raw_data=raw_data, name=self.content.name)
            return movies.video()
