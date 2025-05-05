# -*- coding: utf-8 -*-
import re

from common.trackers.trackers import TRACKData
from unit3dup import pvtTracker
from view import custom_console

class View:

    def __init__(self, tracker_name: str):
        self.tracker = pvtTracker.Unit3d(tracker_name=tracker_name)

        self.perPage = 130
        # Load the constant tracker
        self.tracker_data = TRACKData.load_from_module(tracker_name=tracker_name)
        print()

    def get_unique_id(self, media_info: str) -> str:
        # Divido per campi
        raw_media = media_info.split("\r")
        unique_id = "-" * 40
        if len(raw_media) > 1:
            match = re.search(r"Unique ID\s+:\s+(\d+)", media_info)
            if match:
                unique_id = match.group(1)
        return unique_id

    def print_info(self, tracker_data: dict):
        data = [item for item in tracker_data["data"]]
        for item in data:
            # Ottengo media info
            media_info = item["attributes"]["media_info"]
            unique_id = (
                self.get_unique_id(media_info=media_info) if media_info else "-" * 40
            )
            # console.print o log non stampa info_hash !
            print(
                f"[{str(item['attributes']['release_year'])}] - [{item['attributes']['info_hash']}] [{unique_id}]"
                f" -> {item['attributes']['name']}"
            )

    @staticmethod
    def print_normal(tracker_data: dict):
        data = [item for item in tracker_data["data"]]

        for item in data:
            if item['attributes']['tmdb_id'] != 0:
                if not item['attributes']['release_year']:
                    release_year = 'release year not available'
                else:
                    release_year = item['attributes']['release_year']

                media = f"[TRACKER] TMDB: {item['attributes']['tmdb_id']} - {release_year}"

            else:
                media = f"[TRACKER] IGDB: {item['attributes']['igdb_id']}"

            custom_console.bot_log(f"\n {media} - {item['attributes']['name']}")



    def page_view(self, tracker_data: dict, tracker: pvtTracker, info=False):

        self.print_normal(tracker_data) if not info else self.print_info(tracker_data)
        page = 0
        while True:
            if not tracker_data["links"]["next"]:
                break

            page += 1
            custom_console.bot_question_log(
                f"\n Prossima Pagina '{page}' - Premi un tasto per continuare, Q(quit) - "
            )
            if input().lower() == "q":
                break
            print()
            custom_console.rule(f"\n[bold blue]'Page -> {page}'", style="#ea00d9")
            tracker_data = tracker.next(url=tracker_data["links"]["next"])
            (
                self.print_normal(tracker_data)
                if not info
                else self.print_info(tracker_data)
            )

