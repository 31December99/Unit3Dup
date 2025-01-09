# -*- coding: utf-8 -*-
import guessit
from common.utility.utility import Manage_titles, System
from common.utility import title
from common.constants import my_language
from common.trackers.trackers import ITTData
from common.config import config
from common.custom_console import custom_console
from unit3dup.torrent import Torrent
from unit3dup.contents import Contents
from unit3dup.media_manager.MediaInfoManager import MediaInfoManager


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

    def same_season(self) -> bool:

        # Compare season and episode only if it is a serie
        # Return true if they have at least the same season and episode
        if self.content_file.guessit_season and  self.tracker_file.guessit_season:
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
        return self.same_season()


class Duplicate:

    def __init__(self, content: Contents):

        # User content from the scan process
        self.content: Contents = content

        # Class to get info about a torrent
        self.torrent_info = Torrent()

        # Load the constant tracker
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
        custom_console.bot_log(f"* '{self.guess_filename.guessit_title.upper()}' - Size({self.content_size}GB) -"
                               f" => delta < {self.size_threshold}% = Duplicate *\n")
        return self.search()

    def search(self) -> bool:

        # Search torrent by Name
        tracker_search = self.torrent_info.search(self.guess_filename.guessit_title)

        # Flag for the search results
        already_present = False

        # Compare and return a result
        for t_data in tracker_search["data"]:
            already_present = self._process_tracker_data(t_data)

        # if a result is found, ask the user
        if already_present:
            # Start message prints the size of the user file
            while 1:
                custom_console.bot_question_log(
                    "\nPress (C) to continue, (S) to SKIP.. (Q) Quit - "
                )
                user_answer = input()
                custom_console.rule()

                # Exit
                if "q" == user_answer.lower():
                    exit(1)

                # Choice to continue
                if "c" == user_answer.lower():
                    return False
                # Skip this media
                if "s" == user_answer.lower():
                    return True

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
        # Convert to GB
        size = round(size / (1024 ** 3), 2)
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
        formatted_resolution = f"{resolution:<{self.RESOLUTION_WIDTH}}" if self.category != self.game_category else ''
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
                        # Not a duplicate
                        continue

                # TH_SIZE = 100 %
                # UserFile(GB) - TrackerFile(GB) / max(UserFile,TrackerFile) = DeltaSize  > TH_SIZE ?
                #   25.72      -   2.29          /           25.72           =   91.1%    > 100%    NO (duplicate)
                #   25.72      -   11.26         /           25.72           =   56.4%    > 100%    NO (duplicate)
                #   25.72      -   1.78          /           25.72           =   93.1%    > 100%    NO (duplicate)
                # ->>>>>>> Non supera la differenza (Th_size) da noi impostata - è un duplicate

                # TH_SIZE = 0 %
                # UserFile(GB) - TrackerFile(GB) / max(UserFile,TrackerFile) = DeltaSize   > TH_SIZE ?
                #   25.72      -   2.29          /           25.72           =   91.1 %    > 0%     SI (no duplicate)
                #   25.72      -   11.26         /           25.72           =   56.4%     > 0%     SI (no duplicate)
                #   25.72      -   1.78          /           25.72           =   93.1 %    > 0%     SI (no duplicate)
                # ->>>>>>> Supera la differenza (Th_size) da noi impostata - Non è un duplicate

                    # compare the seasons if it is a serie
                    if self.compare(value=tracker_value, content_file=self.guess_filename):
                        self._print_output(value=tracker_value, delta_size=delta_size)
                        self.flag_already = True

        # At least one media needs to match the tracker database
        return self.flag_already

    @staticmethod
    def compare(value: guessit, content_file: guessit) -> bool:
        return CompareTitles(tracker_file=title.Guessit(value["name"]), content_file=content_file).process()
