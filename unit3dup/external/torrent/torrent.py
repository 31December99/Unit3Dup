# -*- coding: utf-8 -*-

import re
import time
from typing import Any

from unit3dup.external.tracker import pvtTracker
from unit3dup.external.tracker.database import Database
from unit3dup.external.tracker.trackers import TRACKData
from unit3dup.view import custom_console


class Torrent:
    """
    High-level interface for searching and filtering torrents
    on a Unit3D tracker
    """

    def __init__(self, tracker_name: str):
        self.per_page = 100

        self.tracker = pvtTracker.Unit3d(
            tracker_name=tracker_name
        )

        self.database = Database(
            db_file=tracker_name
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def get_unique_id(media_info: str) -> str:
        """
        Extract the Unique ID from a MediaInfo string

        Returns:
            str: Unique ID if found, otherwise 40 dashes
        """

        default_id = "-" * 40

        if not media_info:
            return default_id

        match = re.search(
            r"Unique ID\s+:\s+(\d+)",
            media_info
        )

        return (
            match.group(1)
            if match
            else default_id
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, keyword: str) -> dict[str, Any] | None:
        """
        Search torrents by name
        """

        # The user does not always include '-' in the title.
        keyword = keyword.replace("-", " ")

        return self.tracker.get_name(
            name=keyword,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Text filters
    # ------------------------------------------------------------------

    def get_by_description(
        self,
        description: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_description(
            description=description,
            perPage=self.per_page
        )

    def get_by_bdinfo(
        self,
        bd_info: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_bdinfo(
            bdinfo=bd_info,
            perPage=self.per_page
        )

    def get_by_uploader(
        self,
        username: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_uploader(
            uploader=username,
            perPage=self.per_page
        )

    def get_by_start_year(
        self,
        start_year: str
    ) -> dict[str, Any] | None:

        return self.tracker.after_start_year(
            start_year=start_year,
            perPage=self.per_page
        )

    def get_by_end_year(
        self,
        end_year: str
    ) -> dict[str, Any] | None:

        return self.tracker.before_end_year(
            end_year=end_year,
            perPage=self.per_page
        )

    def get_by_mediainfo(
        self,
        mediainfo: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_mediainfo(
            mediainfo=mediainfo,
            perPage=self.per_page
        )

    def get_by_filename(
        self,
        file_name: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_filename(
            file_name=file_name,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Type / Resolution
    # ------------------------------------------------------------------

    def get_by_types(
        self,
        type_id: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_types(
            type_id=type_id,
            perPage=self.per_page
        )

    def get_by_res(
        self,
        resolution_id: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_res(
            res_id=resolution_id,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # External IDs
    # ------------------------------------------------------------------

    def get_by_tmdb_id(
        self,
        tmdb_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_tmdb(
            tmdb_id=tmdb_id,
            perPage=self.per_page
        )

    def get_by_imdb_id(
        self,
        imdb_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_imdb(
            imdb_id=imdb_id,
            perPage=self.per_page
        )

    def get_by_igdb_id(
        self,
        igdb_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_igdb(
            igdb_id=igdb_id,
            perPage=self.per_page
        )

    def get_by_tvdb_id(
        self,
        tvdb_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_tvdb(
            tvdb_id=tvdb_id,
            perPage=self.per_page
        )

    def get_by_mal_id(
        self,
        mal_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_mal(
            mal_id=mal_id,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Playlist / Collection
    # ------------------------------------------------------------------

    def get_by_playlist_id(
        self,
        playlist_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_playlist_id(
            playlist_id=playlist_id,
            perPage=self.per_page
        )

    def get_by_collection_id(
        self,
        collection_id: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_collection_id(
            collection_id=collection_id,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Torrent properties
    # ------------------------------------------------------------------

    def get_by_freeleech(
        self,
        freeleech: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_freeleech(
            freeleech=freeleech,
            perPage=self.per_page
        )

    def get_by_season(
        self,
        season: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_season_number(
            se_number=season,
            perPage=self.per_page
        )

    def get_by_episode(
        self,
        episode: int
    ) -> dict[str, Any] | None:

        return self.tracker.get_episode_number(
            ep_number=episode,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Status filters
    # ------------------------------------------------------------------

    def get_alive(self) -> dict[str, Any] | None:
        return self.tracker.get_alive(
            alive=True,
            perPage=self.per_page
        )

    def get_dead(self) -> dict[str, Any] | None:
        return self.tracker.get_dead(
            dead=True,
            perPage=self.per_page
        )

    def get_dying(self) -> dict[str, Any] | None:
        return self.tracker.get_dying(
            dying=True,
            perPage=self.per_page
        )

    def get_doubleup(self) -> dict[str, Any] | None:
        return self.tracker.get_double_up(
            double_up=True,
            perPage=self.per_page
        )

    def get_featured(self) -> dict[str, Any] | None:
        return self.tracker.get_featured(
            featured=True,
            perPage=self.per_page
        )

    def get_refundable(self) -> dict[str, Any] | None:
        return self.tracker.get_refundable(
            refundable=True,
            perPage=self.per_page
        )

    def get_stream(self) -> dict[str, Any] | None:
        return self.tracker.get_stream(
            stream=True,
            perPage=self.per_page
        )

    def get_sd(self) -> dict[str, Any] | None:
        return self.tracker.get_sd(
            sd=True,
            perPage=self.per_page
        )

    def get_highspeed(self) -> dict[str, Any] | None:
        return self.tracker.get_highspeed(
            highspeed=True,
            perPage=self.per_page
        )

    def get_internal(self) -> dict[str, Any] | None:
        return self.tracker.get_internal(
            internal=True,
            perPage=self.per_page
        )

    def get_personal(self) -> dict[str, Any] | None:
        return self.tracker.get_personal_release(
            personalRelease=True,
            perPage=self.per_page
        )

    # ------------------------------------------------------------------
    # Combo filters
    # ------------------------------------------------------------------

    def get_by_tmdb_res(
        self,
        tmdb_id: int,
        resolution_id: str
    ) -> dict[str, Any] | None:

        return self.tracker.get_tmdb_res(
            tmdb_id=tmdb_id,
            res_id=resolution_id,
            perPage=self.per_page
        )


class View(Torrent):
    """
    Presentation layer for torrent searches and filters.
    """

    def __init__(self, tracker_name: str):
        super().__init__(
            tracker_name=tracker_name
        )

        self.tracker_data = (
            TRACKData.load_from_module(
                tracker_name=tracker_name
            )
        )

        self.tracker_name = tracker_name

        print()

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------

    def print_info(
        self,
        tracker_data: dict[str, Any]
    ) -> None:
        """
        Print detailed information about torrents.
        """

        for item in tracker_data.get("data", []):
            attributes = item.get(
                "attributes",
                {}
            )

            media_info = attributes.get(
                "media_info",
                ""
            )

            unique_id = self.get_unique_id(
                media_info
            )

            release_year = attributes.get(
                "release_year"
            )

            name = attributes.get(
                "name",
                "Unknown"
            )

            print(
                f"[{release_year}] "
                f"- [{unique_id}] "
                f"-> {name}"
            )

    def print_normal(
        self,
        tracker_data: dict[str, Any],
        save: bool = False
    ) -> None:
        """
        Print normal torrent information.
        """

        for item in tracker_data.get("data", []):
            attributes = item.get(
                "attributes",
                {}
            )

            tmdb_id = attributes.get(
                "tmdb_id",
                0
            )

            igdb_id = attributes.get(
                "igdb_id",
                0
            )

            release_year = attributes.get(
                "release_year"
            )

            name = attributes.get(
                "name",
                "Unknown"
            )

            if tmdb_id != 0:
                release_year = (
                    release_year
                    if release_year
                    else "release year not available"
                )

                media = (
                    f"{self.tracker_name} - "
                    f"TMDB: {tmdb_id} - "
                    f"{release_year}"
                )

            elif igdb_id != 0:
                media = (
                    f"{self.tracker_name} "
                    f"IGDB: {igdb_id}"
                )

            else:
                media = (
                    f"{self.tracker_name} DOC:"
                )

            custom_console.bot_log(
                f"\n {media} - {name}"
            )

            if save:
                self.database.write(
                    attributes
                )

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------

    def page_view(
        self,
        tracker_data: dict[str, Any],
        info: bool = False,
        inkey: bool = True,
        save: bool = False
    ) -> None:
        """
        Display API results page by page.
        """

        if not tracker_data:
            custom_console.bot_warning_log(
                "No results returned by tracker."
            )
            return

        printer = (
            self.print_info
            if info
            else self.print_normal
        )

        printer(
            tracker_data,
            save=save
        ) if not info else printer(
            tracker_data
        )

        page = 0

        while True:
            links = tracker_data.get(
                "links",
                {}
            )

            next_url = links.get(
                "next"
            )

            if not next_url:
                break

            page += 1

            if inkey:
                custom_console.bot_question_log(
                    f"\nProssima pagina '{page}' "
                    f"- Premi un tasto per continuare, "
                    f"Q (quit) - "
                )

                if input().lower() == "q":
                    break

            else:
                # API rate limit protection.
                time.sleep(2)

            print()

            custom_console.rule(
                f"\n[bold blue]'Page -> {page}'",
                style="#ea00d9"
            )

            tracker_data = self.tracker.next(
                url=next_url
            )

            if not tracker_data:
                break

            printer(
                tracker_data,
                save=save
            ) if not info else printer(
                tracker_data
            )

    # ------------------------------------------------------------------
    # Search views
    # ------------------------------------------------------------------

    def view_search(
        self,
        keyword: str,
        info: bool = False,
        inkey: bool = True,
        save: bool = False
    ) -> None:

        tracker_data = self.search(
            keyword=keyword
        )

        custom_console.log(
            f"Searching.. '{keyword}'"
        )

        self.page_view(
            tracker_data=tracker_data,
            info=info,
            inkey=inkey,
            save=save
        )

    def view_by_description(
        self,
        description: str
    ) -> None:

        tracker_data = self.get_by_description(
            description=description
        )

        custom_console.bot_log(
            "Filter by torrent description.. "
            f"'{description.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_bdinfo(
        self,
        bdinfo: str
    ) -> None:

        tracker_data = self.get_by_bdinfo(
            bd_info=bdinfo
        )

        custom_console.bot_log(
            "Filter by torrent BDInfo.. "
            f"'{bdinfo.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_uploader(
        self,
        username: str,
        save: bool = False
    ) -> None:

        tracker_data = self.get_by_uploader(
            username=username
        )

        custom_console.bot_log(
            "Filter by torrent uploader.. "
            f"'{username.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data,
            save=save
        )

    def view_by_start_year(
        self,
        start_year: str
    ) -> None:

        tracker_data = self.get_by_start_year(
            start_year=start_year
        )

        custom_console.bot_log(
            "StartYear torrents.. "
            "Return torrents released after "
            f"or in '{start_year}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_end_year(
        self,
        end_year: str
    ) -> None:

        tracker_data = self.get_by_end_year(
            end_year=end_year
        )

        custom_console.bot_log(
            "EndYear torrents.. "
            "Return torrents released before "
            f"or in '{end_year}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_mediainfo(
        self,
        mediainfo: str
    ) -> None:

        tracker_data = self.get_by_mediainfo(
            mediainfo=mediainfo
        )

        custom_console.bot_log(
            "Mediainfo torrents.. "
            "Filter by MediaInfo.. "
            f"'{mediainfo.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    # ------------------------------------------------------------------
    # Type / Resolution views
    # ------------------------------------------------------------------

    def view_by_types(
        self,
        type_name: str
    ) -> None:

        if type_name not in self.tracker_data.type_id:
            custom_console.bot_error_log(
                f"Type not available for '{type_name}'."
            )

            custom_console.bot_warning_log(
                ";".join(
                    self.tracker_data.type_id.keys()
                )
            )

            return

        type_id = str(
            self.tracker_data.type_id[
                type_name
            ]
        )

        tracker_data = self.get_by_types(
            type_id=type_id
        )

        custom_console.bot_log(
            "Types torrents.. "
            f"Filter by type '{type_name.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_res(
        self,
        res_name: str
    ) -> None:

        if res_name not in self.tracker_data.resolution:
            custom_console.bot_error_log(
                f"Resolution not available "
                f"for '{res_name}'."
            )

            custom_console.bot_warning_log(
                ";".join(
                    self.tracker_data.resolution.keys()
                )
            )

            return

        resolution_id = str(
            self.tracker_data.resolution[
                res_name
            ]
        )

        tracker_data = self.get_by_res(
            resolution_id=resolution_id
        )

        custom_console.bot_log(
            "Resolution torrents.. "
            f"Filter by resolution "
            f"'{res_name.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    # ------------------------------------------------------------------
    # ID filters
    # ------------------------------------------------------------------

    def view_by_filename(
        self,
        file_name: str
    ) -> None:

        tracker_data = self.get_by_filename(
            file_name=file_name
        )

        custom_console.bot_log(
            "Filename torrents.. "
            f"Filter by filename "
            f"'{file_name.upper()}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_tmdb_id(
        self,
        tmdb_id: int
    ) -> None:

        tracker_data = self.get_by_tmdb_id(
            tmdb_id=tmdb_id
        )

        custom_console.bot_log(
            "TMDB torrents.. "
            f"Filter by TMDB '{tmdb_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_imdb_id(
        self,
        imdb_id: int
    ) -> None:

        tracker_data = self.get_by_imdb_id(
            imdb_id=imdb_id
        )

        custom_console.bot_log(
            "IMDB torrents.. "
            f"Filter by IMDB '{imdb_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_tvdb_id(
        self,
        tvdb_id: int
    ) -> None:

        tracker_data = self.get_by_tvdb_id(
            tvdb_id=tvdb_id
        )

        custom_console.bot_log(
            "TVDB torrents.. "
            f"Filter by TVDB '{tvdb_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_mal_id(
        self,
        mal_id: int
    ) -> None:

        tracker_data = self.get_by_mal_id(
            mal_id=mal_id
        )

        custom_console.bot_log(
            "MAL torrents.. "
            f"Filter by MAL '{mal_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    # ------------------------------------------------------------------
    # Playlist / Collection
    # ------------------------------------------------------------------

    def view_by_playlist_id(
        self,
        playlist_id: int
    ) -> None:

        tracker_data = self.get_by_playlist_id(
            playlist_id=playlist_id
        )

        custom_console.bot_log(
            "Playlist torrents.. "
            f"Playlist ID '{playlist_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_collection_id(
        self,
        collection_id: int
    ) -> None:

        tracker_data = self.get_by_collection_id(
            collection_id=collection_id
        )

        custom_console.bot_log(
            "Collection torrents.. "
            f"Collection ID '{collection_id}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    # ------------------------------------------------------------------
    # Torrent filters
    # ------------------------------------------------------------------

    def view_by_freeleech(
        self,
        freeleech: int
    ) -> None:

        tracker_data = self.get_by_freeleech(
            freeleech=freeleech
        )

        custom_console.bot_log(
            "Freeleech torrents.. "
            f"Freeleech '{freeleech}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_season(
        self,
        season: int
    ) -> None:

        tracker_data = self.get_by_season(
            season=season
        )

        custom_console.bot_log(
            f"Season torrents.. '{season}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    def view_by_episode(
        self,
        episode: int
    ) -> None:

        tracker_data = self.get_by_episode(
            episode=episode
        )

        custom_console.bot_log(
            f"Episode torrents.. '{episode}'"
        )

        self.page_view(
            tracker_data=tracker_data
        )

    # ------------------------------------------------------------------
    # Boolean filters
    # ------------------------------------------------------------------

    def view_alive(self) -> None:
        self._view_boolean_filter(
            self.get_alive(),
            "Alive torrents.. "
            "Filter by torrents with 1+ seeders."
        )

    def view_dead(self) -> None:
        self._view_boolean_filter(
            self.get_dead(),
            "Dead torrents.. "
            "Filter by torrents with 0 seeders.",
            info=True
        )

    def view_dying(self) -> None:
        self._view_boolean_filter(
            self.get_dying(),
            "Dying torrents.. "
            "Filter by torrents with 1 seeder "
            "and more than 3 downloads."
        )

    def view_doubleup(self) -> None:
        self._view_boolean_filter(
            self.get_doubleup(),
            "DoubleUp torrents.. "
            "Filter by double upload."
        )

    def view_featured(self) -> None:
        self._view_boolean_filter(
            self.get_featured(),
            "Featured torrents.. "
            "Filter by featured torrents."
        )

    def view_refundable(self) -> None:
        self._view_boolean_filter(
            self.get_refundable(),
            "Refundable torrents.. "
            "Filter by refundable torrents."
        )

    def view_stream(self) -> None:
        self._view_boolean_filter(
            self.get_stream(),
            "Stream torrents.. "
            "Filter by stream-optimised content."
        )

    def view_sd(self) -> None:
        self._view_boolean_filter(
            self.get_sd(),
            "Standard torrents.. "
            "Filter by standard-definition content."
        )

    def view_highspeed(self) -> None:
        self._view_boolean_filter(
            self.get_highspeed(),
            "Highspeed torrents.. "
            "Filter by seedbox seeders."
        )

    def view_internal(self) -> None:
        self._view_boolean_filter(
            self.get_internal(),
            "Internal torrents.. "
            "Filter by internal releases."
        )

    def view_personal(self) -> None:
        self._view_boolean_filter(
            self.get_personal(),
            "Personal Release torrents.. "
            "Filter by uploader-created content."
        )

    # ------------------------------------------------------------------
    # Boolean filter helper
    # ------------------------------------------------------------------

    def _view_boolean_filter(
        self,
        tracker_data: dict[str, Any] | None,
        message: str,
        info: bool = False
    ) -> None:

        custom_console.bot_log(
            message
        )

        if tracker_data:
            self.page_view(
                tracker_data=tracker_data,
                info=info
            )

    # ------------------------------------------------------------------
    # Combo filters
    # ------------------------------------------------------------------

    def view_tmdb_res(
        self,
        tmdb_id: int,
        res_name: str
    ) -> None:
        """
        Filter torrents by TMDB ID and resolution.
        """

        if res_name not in self.tracker_data.resolution:
            custom_console.bot_error_log(
                f"Resolution not available "
                f"for '{res_name}'."
            )

            custom_console.bot_warning_log(
                ";".join(
                    self.tracker_data.resolution.keys()
                )
            )

            return

        resolution_id = str(
            self.tracker_data.resolution[
                res_name
            ]
        )

        tracker_data = self.get_by_tmdb_res(
            tmdb_id=tmdb_id,
            resolution_id=resolution_id
        )

        custom_console.bot_log(
            "TMDB + Resolution torrents.. "
            f"TMDB '{tmdb_id}' - "
            f"Resolution '{res_name.upper()}'"
        )

        if tracker_data:
            self.page_view(
                tracker_data=tracker_data
            )