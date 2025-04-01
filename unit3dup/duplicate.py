# -*- coding: utf-8 -*-
import guessit
from common.utility import ManageTitles, System
from common.trackers.trackers import TRACKData
from common.constants import my_language
from common import title

from view import custom_console

from unit3dup.media_manager.MediaInfoManager import MediaInfoManager
from unit3dup.torrent import Torrent
from unit3dup import config_settings
from unit3dup.media import Media



class CompareTitles:

    def __init__(self, tracker_file: guessit, content_file: guessit):
        self.content_screen_size = 0
        self.tracker_screen_size = 0
        self.tracker_file = tracker_file
        self.content_file = content_file
        self.tracker_date = tracker_file.guessit_year
        self.content_date = content_file.guessit_year
        self.ratio = ManageTitles.fuzzyit(
            content_file.guessit_title, tracker_file.guessit_title
        )

    def same_season(self) -> bool:

        # Compare season and episode only if it is a serie
        # Return true if they have at least the same season and episode
        if self.content_file.guessit_season and self.tracker_file.guessit_season:
            same_season = self.content_file.guessit_season == self.tracker_file.guessit_season
            same_episode = self.content_file.guessit_episode == self.tracker_file.guessit_episode
            return same_season and same_episode
        else:
            # always return true if it's a movie
            return True


    # not used
    def is_best_resolution(self) -> bool:
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
        if self.ratio > 49:
            return self.same_season()
        return False



class Duplicate:

    def __init__(self, content: Media, tracker_name: str):

        # User content from the scan process
        self.content: Media = content

        # Class to get info about a torrent
        self.torrent_info = Torrent(tracker_name=tracker_name)

        # Load the constant tracker
        tracker_data = TRACKData.load_from_module(tracker_name=tracker_name)

        # Resolutions
        self.resolutions = tracker_data.resolution

        # Category Movie
        self.movie_category = tracker_data.category.get("movie")

        # Category TvShow
        self.serie_category = tracker_data.category.get("tvshow")

        # Category Game
        self.game_category = tracker_data.category.get("game")

        # Category Doc
        self.docu_category = tracker_data.category.get("edicola")

        # Category that comes for the User's media
        self.category = content.category

        # the user torrent title
        self.guess_filename = title.Guessit(self.content.display_name)

        # convert the user preferred language to iso
        self.preferred_lang = my_language(config_settings.user_preferences.PREFERRED_LANG)

        # Size of the user's content
        self.content_size, self.size_unit = System.get_size(content.torrent_path)

        # Determine how much differs from the user's media size
        self.size_threshold = config_settings.user_preferences.SIZE_TH

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
        # Compare and return a result
        for t_data in tracker_search["data"]:
            # if a result is found, ask the user or autoskip
            if self._process_tracker_data(t_data):
                if not config_settings.user_preferences.SKIP_DUPLICATE:
                    try:
                        while True:
                            custom_console.bot_question_log(
                                "\nPress (C) to continue, (S) to SKIP.. (Q) Quit - "
                            )
                            user_answer = input()
                            # Exit
                            if "q" == user_answer.lower():
                                exit(1)

                            # Choice to continue
                            if "c" == user_answer.lower():
                                return False
                            # Skip this media
                            if "s" == user_answer.lower():
                                return True
                    except KeyboardInterrupt:
                        custom_console.bot_error_log("\nOperation cancelled. Bye !")
                        exit(1)
                else: # if skip_duplicate is on -> autoskip
                    return True
        return False



    def get_resolution_by_num(self, res_id: int) -> str:
        return next((key for key, value in self.resolutions.items() if value == res_id), None)

    def _calculate_threshold(self, size: int) -> int:
        # Size in GB
        # Skip duplicate check if the size is out of the threshold

        size = round(size / (1024 ** 3), 2) if self.size_unit == 'GB' else round(size / (1024 ** 2), 2)
        return round(abs(self.content_size - size) / max(self.content_size, size) * 100)

    def _print_output(self, value: dict, delta_size: int, size_th: int):

        name = value["name"]
        resolution = value.get("resolution", "[n/a]")
        size = value.get("size", 0)
        # Convert to GB
        size = round(size / (1024 ** 3), 2)
        tmdb_id = value.get("tmdb_id", 0)
        igdb_id = value.get("igdb_id", 0)

        if self.category != self.game_category:
            mediainfo_manager = MediaInfoManager(media_info_output=value)
            languages = mediainfo_manager.languages.upper()
        else:
            languages = "[n/a]"

        formatted_tmdb_id = f"{tmdb_id:>{self.TMDB_ID_WIDTH}}"
        formatted_igdb_id = f"{igdb_id:>{self.IGDB_ID_WIDTH}}"
        formatted_size = f"{size:>{self.SIZE_WIDTH}.2f} GB"
        formatted_name = f"{name:<{self.NAME_WIDTH}}"
        formatted_resolution = f"{resolution:<{self.RESOLUTION_WIDTH}}" if resolution else ''
        formatted_size_th = f"{delta_size:<{self.DELTA_SIZE_WIDTH}}"

        if self.category in {'movie', 'tv'}:
            output = (
                f"-'Duplicate' TMDB-ID {formatted_tmdb_id} - "
                f"{formatted_size} delta={formatted_size_th}% - "
                f"{formatted_resolution}' "
                f"{formatted_name} "
                f"{languages}'"
            )
        else:
            output = (
                f"- IGDB-ID {formatted_igdb_id} - "
                f"{formatted_size} delta={formatted_size_th}% - "
                f"{formatted_name}"
            )

        custom_console.bot_log(f"Your file: '{self.content.display_name}' Size: {self.content_size} GB - "
                                       f"Size_TH: {size_th}%")
        custom_console.bot_log(output)

    def _process_tracker_data(self, data_from_the_tracker) -> bool:

        if CompareTitles(tracker_file=title.Guessit(data_from_the_tracker['attributes']['name']),
                         content_file=self.guess_filename).process():

            delta_size = self._calculate_threshold(size=data_from_the_tracker['attributes']["size"])
            if delta_size > config_settings.user_preferences.SIZE_TH:
                # Not a Duplicate
                return False
            else:
                self._print_output(value=data_from_the_tracker['attributes'], delta_size=delta_size,
                                   size_th = config_settings.user_preferences.SIZE_TH)
                return True

        return False