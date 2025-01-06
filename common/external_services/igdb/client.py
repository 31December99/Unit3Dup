# -*- coding: utf-8 -*-
import pprint

from thefuzz import fuzz
from rich.align import Align
from rich.table import Table
from common.external_services.igdb.core.api import IGDBapi
from common.external_services.igdb.core.platformid import platform_id
from common.external_services.igdb.core.models.search import Game
from common.custom_console import custom_console


class IGDBViewer:
    def __init__(self):
        pass

    @staticmethod
    def view_results(igdb_results: list['Game']):

        table = Table(
            style="dim",
            title_style="bold yellow",
        )
        table.add_column("Index", style="violet", header_style="bold violet", justify="center")
        table.add_column("IGDB ID", style="blue", header_style="blue", justify="center")
        table.add_column("NAME", style="violet", header_style="violet")
        table.add_column("SUMMARY", style="blue", header_style="blue")

        # Printa a table to present the results
        for index, result in enumerate(igdb_results):
            table.add_row(
                str(index),
                str(result.id),
                f"{result.name} {result.url}",
                result.summary,
            )

        custom_console.bot_log(Align.center(table))

    @staticmethod
    def to_game(results: list) -> list['Game']:

        if results:
            return [
                Game(
                    id=game_data.get('id'),
                    name=game_data.get('name'),
                    summary=game_data.get('summary'),
                    videos=game_data.get('videos', []),
                    url=game_data.get('url','N'),
                )
                for game_data in results
            ]



    def select_result(self, results: list) -> int:
        # Build a menù and ask user to choice a result
        custom_console.bot_log("\nResults:")
        if results:
            while True:
                result = self.input_manager("\nChoice a result to send to the tracker"
                                            " or digit your IGDB number (Q=exit) ")
                # Range between first and last result
                if 0 <= result < len(results):
                    custom_console.bot_log(f"Selected: {result}")
                    return result

                if result >= len(results):
                    return result

    @staticmethod
    def input_manager(input_message: str) -> int:
        while True:
            custom_console.print(input_message, end='', style='violet bold')
            user_choice = input()
            if user_choice.upper() == "Q":
                exit(1)
            if user_choice.isdigit():
                user_choice = int(user_choice)
                if user_choice < 999999:
                    return user_choice


class IGDBClient:

    def __init__(self):
        self.igdb = IGDBapi()
        self.viewer = IGDBViewer()

        # Filter by category to include main games, DLCs, remakes, remasters, expansions, and expanded games
        self.category_filter = "category = (0, 1, 2, 8, 9, 10)"

        self.queries = {
            "media" : "fields game,name,video_id; where id = {video_id};",
            "title" : 'fields id,name,summary,videos; search "{title}";'
                      ' where platforms = ({platform_name}) & {category_filter};',
            "title_no_platform": 'fields id,name,summary,videos; search "{title}";',
        }

    def connect(self)-> bool:
        return self.igdb.login()


    def trailers(self, videos_id: list)-> list:
        return [
            response[0].get('video_id', None)
            for video_id in videos_id
            if (response := self.igdb.request(query=self.queries['media'].format(video_id=video_id),
                                              endpoint="game_videos")) is not None
        ]

    def game_description(self, mygame: Game)-> Game:

        trailers_id = self.trailers(mygame.videos)
        bbcode = mygame.summary
        bbcode += "\n\n[b]Game Trailers:[/b]\n"

        if trailers_id:
            for video_id in trailers_id:
                bbcode += (f"\n[b][spoiler=Spoiler: PLAY GAME TRAILER][center][youtube]{video_id}"
                           f"[/youtube][/center][/spoiler][/b]\n")
        else:
            bbcode+="\nNo trailers available.\n"

        mygame.description = bbcode
        return mygame


    def search(self, title: str, platform_name: str)-> list:
        return self.igdb.request(query=f'fields id,name,summary,videos,platforms,url; search "{title}";'
                                       f' where platforms = ({platform_name}) & ({self.category_filter});',
                                 endpoint="games")

    def search_no_platform(self, title: str)-> list:
        return self.igdb.request(query=f'fields id,name,summary,videos,platforms,url; search "{title}";',endpoint="games")

    def search_by_id(self, igdb_id: int)-> list:
        return self.igdb.request(query=f'fields id,name,summary,videos,url; where id = {igdb_id};',endpoint="games")


    def game(self, game_title: str, platform_list = None)-> Game | None:

        igdb_results=[]
        # Try searching with the specified platform
        if platform_list:
            # Get the platform ID
            for tag in platform_list:
                platform = platform_id.get(tag.upper(), None)
                if platform:
                    igdb_results = self.search(title=game_title, platform_name=platform)

        if not igdb_results:
            # Try without the platform
            igdb_results = self.search_no_platform(title=game_title)

        if not igdb_results:
            # Try a broader search...
            split_title = game_title.split()
            igdb_results = self.search_no_platform(title=split_title[0]) if len(split_title) > 1 else []

        # Choice similar if list is greater than one
        igdb_results = (self.similar(igdb_results=igdb_results, game_title=game_title)
                        if len(igdb_results) > 1 else igdb_results)

        if not igdb_results:
            return
        # Show the results to user
        self.viewer.view_results(igdb_results=self.viewer.to_game(igdb_results))
        while True:
            # ask user to choice
            user_choice = self.viewer.select_result(igdb_results)
            # User chooses to provide a personal IGDB ID
            if user_choice >= len(igdb_results):
               user_result = self.search_by_id(igdb_id=user_choice)
               if user_result:
                   # Only one game was chosen from the menù
                   mygame =  self.viewer.to_game(user_result)
                   # Add a description
                   mygame = self.game_description(mygame=mygame[0])
                   custom_console.bot_log(" - IGDB Found -")
                   self.viewer.view_results(igdb_results=[mygame])
                   custom_console.bot_input_log("Press a button to continue..")
                   input()
                   return mygame
               else:
                   # Wrong IGDB ID
                   custom_console.bot_question_log("* IGDB Not found * Re-try\n")
            else:
                # User makes their choices
                mygame = self.viewer.to_game(igdb_results)
                # Add a description
                mygame = self.game_description(mygame=mygame[0])
                return mygame


    @staticmethod
    def similar(igdb_results: list, game_title: str):

        game_title_start_word = game_title.split()[0].lower()
        threshold = 80
        while True:
            jaro = [
                game
                for game in igdb_results
                if (fuzz.WRatio(game['name'].lower(), game_title)) > threshold
            ]
            if jaro or threshold < 0:
                break
            else:
                threshold-= 10

        # A words at least in results: es. 'gta' results -> 'Grand Theft Auto' no gta words present
        matches = [title for title in jaro if game_title.split()[0].lower() in title['name'].lower()]
        if matches:
            return [title for title in jaro if title['name'].lower().startswith(game_title_start_word)]
        else:
            return jaro

