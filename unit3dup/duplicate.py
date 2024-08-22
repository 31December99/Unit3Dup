# -*- coding: utf-8 -*-
import guessit

from unit3dup.torrent import Torrent
from unit3dup.contents import Contents
from rich.console import Console
from unit3dup import title
from unit3dup.search import TvShow
from unit3dup import config
from unit3dup.utility import Manage_titles, System

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
        for data in self.raw_data["data"]:
            file_name = data["attributes"]["files"][0]["name"]
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
        for data in self.raw_data["data"]:
            file_name = data["attributes"]["files"][0]["name"]
            guess_filename_tracker = title.Guessit(file_name).guessit_title
            guess_filename_content = title.Guessit(self.name).guessit_title
            if guess_filename_content.lower() == guess_filename_tracker.lower():
                return True
        return False


class CompareTitles:

    def __init__(self, tracker_file: guessit, content_file: guessit):
        self.content_screen_size = 0
        self.tracker_screen_size = 0
        self.tracker_file = tracker_file
        self.content_file = content_file
        self.tracker_date = tracker_file.guessit_year
        self.content_date = content_file.guessit_year
        self.ratio = Manage_titles.fuzzyit(
            content_file.guessit_title, tracker_file.guessit_title
        )

    def same_date(self):
        return self.content_date == self.tracker_date or self.content_date is None or self.tracker_date is None

    def is_greater95(self) -> bool:
        return True if self.ratio > 95 else False

    def is_best_resolution(self):
        if self.tracker_file.screen_size:
            self.tracker_screen_size = int(
                self.tracker_file.screen_size.lower().replace("p", "")
            )
        if self.content_file.screen_size:
            self.content_screen_size = int(
                self.content_file.screen_size.lower().replace("p", "")
            )
        return False

    def process(self) -> bool:
        # Same date, or both may be None
        if self.same_date():
            if self.is_greater95():
                return True
            else:
                return False
        else:
            return False


class Duplicate:

    def __init__(self, content: Contents):
        self.content: Contents = content
        self.torrent_info = Torrent()
        self.config = config.trackers.get_tracker(tracker_name=content.tracker_name)
        self.movie_category = self.config.tracker_values.category("movie")
        self.serie_category = self.config.tracker_values.category("tvshow")
        self.guess_filename = title.Guessit(self.content.display_name)
        self.flag_already = False
        self.content_size = System.get_size(content.torrent_path)

    def process(self, tmdb_id: str) -> bool:
        return self.search()

    def search(self) -> bool:
        tracker_data = self.torrent_info.search(self.guess_filename.guessit_title)
        already_present = False
        console.rule(
            f"Searching for duplicate -> Your Files: [{self.content_size} GB]"
            f" '{self.content.torrent_path}'",
            style="green bold",
        )
        for t_data in tracker_data["data"]:
            already_present = self._view_data(t_data)
        if already_present:
            while 1:
                console.print(
                    "\nPress (C) to continue, (S) to SKIP.. (Q) Quit - ", end=""
                )
                user_answer = input()
                if "c" == user_answer.lower():
                    return False
                if "s" == user_answer.lower():
                    return True
                if "q" == user_answer.lower():
                    exit(1)

    def _view_data(self, data: dict) -> bool:

        for key, value in data.items():
            if "attributes" in key:
                if value["category_id"] == self.movie_category or value["category_id"] == self.serie_category:

                    name = value["name"]
                    resolution = value["resolution"]
                    info_hash = value["info_hash"]

                    # Size in GB
                    size = round(value["size"] / (1024 ** 3), 2)
                    tmdb_id = value["tmdb_id"]
                    tracker_file_name = title.Guessit(name)
                    already = self.compare(
                        tracker_file=tracker_file_name, content_file=self.guess_filename
                    )

                    # Format field
                    tmdb_id_width = 6
                    size_width = 6
                    name_width = 30
                    resolution_width = 5
                    info_hash_width = 20
                    formatted_tmdb_id = f"{tmdb_id:>{tmdb_id_width}}"
                    formatted_size = f"{size:>{size_width}.2f} GB"
                    formatted_name = f"{name:<{name_width}}"
                    formatted_resolution = f"{resolution:<{resolution_width}}"
                    formatted_info_hash = f"{info_hash:<{info_hash_width}}"

                    if already:
                        console.log(
                            f"[TMDB-ID {formatted_tmdb_id}] [{formatted_size}] '[HASH {formatted_info_hash}]"
                            f" [{formatted_resolution}]' {formatted_name}"
                        )

                        self.flag_already = True
        # At least one media needs to match the tracker database
        return self.flag_already

    def compare(self, tracker_file: guessit, content_file: guessit) -> bool:
        already = CompareTitles(tracker_file=tracker_file, content_file=content_file)
        return already.process()

    # not used
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
