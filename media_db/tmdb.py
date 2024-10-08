# -*- coding: utf-8 -*-
import sys
import tmdbv3api.exceptions

from common.custom_console import custom_console
from common.utility.utility import Manage_titles
from tmdbv3api import TMDb, Movie, TV, Season
from unit3dup.contents import Contents
from media_db.results import Results
from common.config import config
from unidecode import unidecode
from thefuzz import fuzz


class MyTmdb:

    def __init__(self, table: str, content: Contents, year="", videoid=""):
        self.table = table
        self.content = content
        self.ext_title = None
        self.year = year
        self.videoid = videoid
        self.tmdb = None
        self._tmdb = TMDb()
        self._tmdb.language = "it-EN"
        self._tmdb.api_key = config.TMDB_APIKEY
        self.__mv_tmdb = Movie()
        self.__tv_tmdb = TV()
        self.season = Season()
        self.__result = None
        self.__page = []
        self.file_name = content.file_name
        self.episode_title: str | None = None

        if self.table == "Serie":
            self.tmdb = self.__tv_tmdb

        if self.table == "Movie":
            self.tmdb = self.__mv_tmdb

    def search(self, ext_title: str):
        self.ext_title = ext_title.lower()
        self.ext_title = self.ext_title.replace("-", " ")
        self.ext_title = self.ext_title.replace("–", " ")
        self.ext_title = self.ext_title.replace("’", " ")
        self.ext_title = self.ext_title.replace("'", " ")
        # custom_console.bot_log(f"\n[TMDB Search]..........  {self.ext_title}")

        try:
            self.__requests()
        except tmdbv3api.exceptions.TMDbException as e:
            custom_console.bot_error_log(f"[TMDB] '{e}'")
            sys.exit()

        result = self.__search_titles()
        if not result:
            result = self.__search_alternative()
            if not result:
                result = self.__search_translations()
                if not result:
                    return None
        else:
            # Search the episode name in seasons details and remove it from the filename content
            details, result.keywords = self.keywords(result.video_id)
            if self.table == "Serie":
                season_details = self.season.details(result.video_id, self.content.season)
                episodes = season_details["episodes"]
                for episode in episodes:
                    if episode["episode_number"] == self.content.episode:
                        self.episode_title = Manage_titles.clean(episode["name"])
        return result

    def input_tmdb(self) -> Results:
        custom_console.bot_log(
            f"[red reverse]{self.file_name}[/red reverse] Unable to identify the TMDB ID."
            f" Please enter the tmdb ID number.."
        )
        results = Results()
        while True:
            tmdb_id = input(f"> ")
            if not tmdb_id.isdigit():
                custom_console.bot_error_log(
                    f"I do not recognize {tmdb_id} as a number. Please try again.."
                )
                continue
            custom_console.bot_log(f"You have entered {tmdb_id}")
            user_answ = input("Are you sure ? (y/n)> ")
            keywords = ""
            if "y" == user_answ.lower():
                # Zero = No TMDB ID
                if tmdb_id != "0":
                    details, keywords = self.keywords(int(tmdb_id))
                    # Keywords
                    if keywords:
                        results.keywords = keywords
                    # If details then return the tmdb_id
                    if details:
                        results.poster_path = details["poster_path"]
                        results.backdrop_path = details["backdrop_path"]
                        results.video_id = tmdb_id
                        return results
                else:
                    results.video_id = 0
                    return results

    def __requests(self):
        self.__result = self.tmdb.search(self.ext_title)
        # custom_console.bot_log(f"[TMDB total-results]...  {self.__result['total_results']}")
        # custom_console.bot_log(f"[TMDB total-pages].....  {self.__result['total_pages']}")
        if self.__result["total_results"] > 0:
            for result in self.__result:
                results = Results()
                try:
                    if isinstance(self.tmdb, TV):
                        # Solo per tmdb esclude type (web-dl ecc)
                        results.title = result["name"].replace("-", " ").lower()
                        results.title = results.title.replace("–", " ")
                        results.title = results.title.replace("’", " ")
                        results.title = results.title.replace("'", " ")

                        results.original_title = (
                            result["original_name"].replace("-", " ").lower()
                        )
                        results.original_title = results.original_title.replace(
                            "–", " "
                        )
                        results.original_title = results.original_title.replace(
                            "’", " "
                        )
                        results.original_title = results.original_title.replace(
                            "'", " "
                        )
                        results.date = result["first_air_date"]

                    if isinstance(self.tmdb, Movie):
                        # Solo per tmdb esclude type (web-dl ecc)
                        results.title = result["title"].replace("-", " ").lower()
                        results.title = results.title.replace("–", " ")
                        results.title = results.title.replace("’", " ")
                        results.title = results.title.replace("'", " ")

                        results.original_title = (
                            result["original_title"].replace("-", " ").lower()
                        )
                        results.original_title = results.original_title.replace(
                            "–", " "
                        )
                        results.original_title = results.original_title.replace(
                            "’", " "
                        )
                        results.original_title = results.original_title.replace(
                            "'", " "
                        )
                        results.date = getattr(result, "release_date", "")

                    # ALL
                    results.genre_ids = getattr(result, "genre_ids", "")
                    results.video_id = result["id"]
                    results.poster_path = result["poster_path"]
                    results.backdrop_path = result["backdrop_path"]
                    results.overview = result["overview"]
                    results.popularity = getattr(result, "popularity", "")
                    details = self.tmdb.details(result["id"])
                    if "translations" in details:
                        for iso in details["translations"]["translations"]:
                            results.translations.append(iso)
                        results.alternative.append(
                            self.tmdb.alternative_titles(result["id"])
                        )

                except tmdbv3api.exceptions.TMDbException as e:
                    results.translations = []
                    results.alternative = []
                self.__page.append(results)

    def details(self, video_id: str):
        return self.tmdb.details(video_id)

    def __search_alternative(self):
        field = "titles" if isinstance(self.tmdb, Movie) else "results"
        # print(f".:: ALTERNATIVE n°{len(self.__page)} ::.")
        for index, page in enumerate(self.__page):
            for iso in page.alternative:
                results = iso[field]
                ext_title = Manage_titles.clean(unidecode(self.ext_title))
                if len(iso[field]) > 0:
                    for result in results:
                        title = Manage_titles.clean(unidecode(result["title"]))
                        # print(f"EXT_T: {ext_title} = ALTERNATIVE TITLE: {title}")
                        if ext_title == title:
                            return page
                        else:
                            ratio = fuzz.ratio(ext_title, title)
                            # print(f"EXT_T: {ext_title} VS ALTERNATIVE TITLE: {title} RATIO: {ratio}\n")
                            if ratio > 95:
                                return page

    def __search_titles(self):
        """
        compare the title of each result on the page with the input title
        """
        # print(f".:: SEARCH_TITLES RESULT n°{len(self.__page)} ::.")
        for index, page in enumerate(self.__page):
            original_title = Manage_titles.clean(
                Manage_titles.accented_remove(page.original_title)
            )
            title = Manage_titles.clean(Manage_titles.accented_remove(page.title))
            ext_title = Manage_titles.clean(
                Manage_titles.accented_remove(self.ext_title)
            )
            if original_title:
                # print(f"EXT_T: {ext_title} = ORIGINAL TITLE: {original_title}")
                if ext_title == original_title:
                    return page
                else:
                    ratio = fuzz.ratio(ext_title, original_title)
                    # print(f"EXT_T: {ext_title} VS ORIGINAL TITLE: {original_title} RATIO: {ratio}\n")
                    if ratio > 95:
                        return page
            if title:
                # print(f"EXT_T: {ext_title} = TITLE: {title}")
                if ext_title == title:
                    return page
                else:
                    ratio = fuzz.ratio(ext_title, title)
                    # print(f"EXT_T: {ext_title} VS TITLE: {title} RATIO: {ratio}\n")
                    if ratio > 95:
                        return page

    def __search_translations(self):
        """
         compare the translations of each result on the page with the input title
        :return:
        """
        # print(f".:: TRANSLATION n°{len(self.__page)} ::.")
        for index, page in enumerate(self.__page):
            for translation in page.translations:
                if "title" in translation["data"]:
                    name = translation["data"].get("title", "")
                else:
                    name = translation["data"].get("name", "")
                name = Manage_titles.clean(unidecode(name)).lower()
                tagline = Manage_titles.clean(
                    Manage_titles.accented_remove(translation["data"]["tagline"])
                ).lower()
                ext_title = Manage_titles.clean(unidecode(self.ext_title))

                name = name.replace("-", " ")
                name = name.replace("–", " ")
                name = name.replace("’", " ")
                name = name.replace("'", " ")

                tagline = tagline.replace("-", " ")
                tagline = tagline.replace("–", " ")
                tagline = tagline.replace("’", " ")
                tagline = tagline.replace("'", " ")

                if name:
                    if ext_title == name:
                        # todo aggiungere anche confronto con Year ?
                        return page
                    else:
                        ratio = fuzz.ratio(ext_title, name)
                        # print(f"EXT_T: {ext_title} VS TRANSLATION NAME {name} RATIO {ratio}\n")
                        if ratio > 95:
                            return page
                if tagline:
                    if ext_title == tagline:
                        # print(f"EXT_T: {ext_title} = TAGLINE {tagline} ?")
                        if self.ext_title in tagline:
                            # todo aggiungere anche confronto con Year ?
                            return page
                        else:
                            ratio = fuzz.ratio(ext_title, tagline)
                            # print(f"EXT_T: {ext_title} = TAGLINE {tagline} RATIO {ratio}\n")
                            if ratio > 95:
                                return page

    def keywords(self, video_id: int) -> (str, str):
        try:
            details = self.tmdb.details(video_id)
        except tmdbv3api.exceptions.TMDbException as e:
            custom_console.bot_error_log(f"Keywords - {video_id} - Report it {e} ")
            exit(1)
        if "keywords" in details:
            keywords = details.keywords
            if keywords["keywords"]:
                keywords = ",".join([key["name"] for key in keywords["keywords"]])
        else:
            keywords = None
        return details, keywords
