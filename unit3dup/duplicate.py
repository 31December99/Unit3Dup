# -*- coding: utf-8 -*-
import guessit

from media_db.search import TvShow
from common.utility.utility import Manage_titles, System
from common.utility import title
from common.constants import my_language
from common.trackers.trackers import ITTData
from common.config import config
from common.custom_console import custom_console
from unit3dup.torrent import Torrent
from unit3dup.contents import Contents
from unit3dup.media_manager.MediaInfoManager import MediaInfoManager


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
        return (
            self.content_date == self.tracker_date
            or self.content_date is None
            or self.tracker_date is None
        )

    def is_greater95(self) -> bool:
        return True if self.ratio > 95 else False

    # not used
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

        # User content from the scan process
        self.content: Contents = content

        # Class to get info about a torrent
        self.torrent_info = Torrent()

        # Load the constants tracker
        tracker_data = ITTData.load_from_module()

        # Category Movie
        self.movie_category = tracker_data.category.get("movie")

        # Category TvShow
        self.serie_category = tracker_data.category.get("tvshow")

        # Category Game
        self.game_category = tracker_data.category.get("game")

        # Category that comes for the User's media
        self.category = content.category

        # the user torrent title
        self.guess_filename = title.Guessit(self.content.display_name)

        # Size of the user's content
        self.content_size = System.get_size(content.torrent_path)

        # convert the user preferred language to iso
        self.preferred_lang = my_language(config.PREFERRED_LANG)

        # Determine how much differs from the user's media size
        self.size_threshold = config.SIZE_TH

        # Final result
        self.flag_already = False

        # For printing output
        self.TMDB_ID_WIDTH = 6
        self.IGDB_ID_WIDTH = 6
        self.SIZE_WIDTH = 4
        self.NAME_WIDTH = 30
        self.RESOLUTION_WIDTH = 5
        self.INFO_HASH_WIDTH = 40
        self.DELTA_SIZE_WIDTH = 2

    def process(self) -> bool:
        return self.search()

    def search(self) -> bool:

        # Search torrent by Name
        tracker_search = self.torrent_info.search(self.guess_filename.guessit_title)

        # Flag for the search results
        already_present = False

        # Start message prints the size of the user file
        custom_console.panel_message(
            f"Searching for duplicate {self.content.torrent_path} [{self.content_size} GB]"
        )

        # Compare and return a result
        for t_data in tracker_search["data"]:
            already_present = self._process_tracker_data(t_data)

        # if a result is found ask the user
        if already_present:
            while 1:
                custom_console.bot_question_log(
                    "\nPress (C) to continue, (S) to SKIP.. (Q) Quit - "
                )
                user_answer = input()
                # Choice to continue
                if "c" == user_answer.lower():
                    return False
                # Skip this media
                if "s" == user_answer.lower():
                    return True
                # Exit
                if "q" == user_answer.lower():
                    exit(1)

    def _calculate_threshold(self, size: int) -> int:
        # Size in GB
        # Skip duplicate check if the size is out of the threshold
        size = round(size / (1024**3), 2)
        return round(abs(self.content_size - size) / max(self.content_size, size) * 100)

    def _print_output(self, value: dict, delta_size: int):

        name = value["name"]
        resolution = value.get("resolution", "[n/a]")
        info_hash = value.get("info_hash", 0)
        size = value.get("size", 0)
        tmdb_id = value.get("tmdb_id", 0)
        igdb_id = value.get("igdb_id", 0)

        if self.category != self.game_category:
            mediainfo_manager = MediaInfoManager(media_info_output=value)
            languages = (
                mediainfo_manager.languages.upper()
                if mediainfo_manager.languages
                else "N/A"
            )
        else:
            languages = "[n/a]"

        formatted_tmdb_id = f"{tmdb_id:>{self.TMDB_ID_WIDTH}}"
        formatted_igdb_id = f"{igdb_id:>{self.IGDB_ID_WIDTH}}"
        formatted_size = f"{size:>{self.SIZE_WIDTH}.2f} GB"
        formatted_name = f"{name:<{self.NAME_WIDTH}}"
        formatted_resolution = f"{resolution:<{self.RESOLUTION_WIDTH}}"
        formatted_info_hash = f"{info_hash:<{self.INFO_HASH_WIDTH}}"
        formatted_size_th = f"{delta_size:<{self.DELTA_SIZE_WIDTH}}"

        if tmdb_id != 0:
            output = (
                f"[TMDB-ID {formatted_tmdb_id}] "
                f"[{formatted_size} delta={formatted_size_th}%] "
                f"'[HASH {formatted_info_hash}]' "
                f"[{formatted_resolution}]' "
                f"{formatted_name},"
                f"[{languages}]'"
            )
        else:
            output = (
                f"[IGDB-ID {formatted_igdb_id}] "
                f"[{formatted_size} delta={formatted_size_th}%] "
                f"'[HASH {formatted_info_hash}]' "
                f"{formatted_name},"
            )

        custom_console.bot_log(output)

    def _process_tracker_data(self, data_from_the_tracker: dict) -> bool:
        for key, tracker_value in data_from_the_tracker.items():
            if "attributes" in key:
                if (
                    tracker_value["category_id"] == self.movie_category
                    or tracker_value["category_id"] == self.serie_category
                    or tracker_value["category_id"] == self.game_category
                ):

                    delta_size = self._calculate_threshold(size=tracker_value["size"])
                    if delta_size > config.SIZE_TH:
                        continue

                    already = self.compare(
                        value=tracker_value, content_file=self.guess_filename
                    )
                    if already:
                        self._print_output(value=tracker_value, delta_size=delta_size)
                        self.flag_already = True

        # At least one media needs to match the tracker database
        return self.flag_already

    @staticmethod
    def compare(value: guessit, content_file: guessit) -> bool:
        name = value["name"]
        already = CompareTitles(
            tracker_file=title.Guessit(name), content_file=content_file
        )
        return already.process()

    # not used
    """
    def search_by_tmdb(self, tmdb_id: int) -> bool:
        # Search media by tmdb id on the tracker

        # Request results from the video online database
        # Get Season
        season = self.guess_filename.guessit_season

        # Get episode
        episode = self.guess_filename.guessit_episode

        # Search for local files in tmdb
        my_tmdb = TvShow(self.content)

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
    """
