# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from rich.align import Align
from common.custom_console import custom_console
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common.external_services.igdb.core.models.game import Game
from common.external_services.igdb.core.platformid import platform_id
from common.config import config
from rich.table import Table

base_request_url = "https://api.igdb.com/v4/"
oauth = "https://id.twitch.tv/oauth2/token"


class IGdbServiceApi:
    token_type: str = ""
    expires: str = ""
    access_token: str = ""
    http_client = None

    @classmethod
    def initialize_http_client(cls):
        if cls.http_client is None:
            headers = Agent.headers()
            headers.update({"Content-Type": "application/x-www-form-urlencoded"})
            cls.http_client = MyHttp(headers)

    @classmethod
    def cls_login(cls) -> bool:
        cls.initialize_http_client()

        params = {
            "client_id": config.IGDB_CLIENT_ID,
            "client_secret": config.IGDB_ID_SECRET,
            "grant_type": "client_credentials",
        }

        if not config.IGDB_CLIENT_ID:
            custom_console.bot_question_log("No IGDB_CLIENT_ID provided\n")
            return False

        if not config.IGDB_ID_SECRET:
            custom_console.bot_question_log("No IGDB_ID_SECRET provided\n")
            return False

        response = cls.http_client.get_url(oauth, params=params, get_method=False)
        if response:
            authentication = response.json()
            cls.access_token = authentication["access_token"]
            cls.expires = authentication["expires_in"]
            cls.token_type = authentication["token_type"]
            custom_console.bot_log("IGDB Login successful!")
            return True
        else:
            custom_console.bot_error_log("Failed to authenticate with IGDB.\n")
            custom_console.bot_error_log("IGDB Login failed. Please check your credentials")
            return False

    def request(self, title: str, platform: list) -> Game | None:
        self.initialize_http_client()

        if not self.access_token:
            custom_console.bot_question_log("Login required. Please login first.\n")
            if not IGdbServiceApi.cls_login():
                custom_console.bot_question_log("Login failed.\n")
                return None

        # Normalize the title by replacing underscores with spaces
        normalized_title = title.replace("_", " ")
        custom_console.bot_log(f"\nNormalized title: '{normalized_title}'")

        platform_name = ""
        # Determine the platform name if provided
        if platform:
            custom_console.bot_log(f"PLATFORM: {platform}")
            if platform[0].upper() in platform_id:
                platform_name = platform_id[platform[0].upper()]
            else:
                custom_console.rule()
                custom_console.bot_error_log(
                    f"\nPlatform {platform} name not found in the BOT database "
                    f"for the title '{title}'\n"
                    f"Please report or add it"
                )
                exit(1)

        # Perform initial search with the specified platform
        custom_console.bot_log(
            f"Searching for title: '{normalized_title}' on platform: '{platform_name}'\n"
        )
        result = self._query(title=normalized_title, platform_name=platform_name)

        # If no results are found, try without platform
        if not result and platform_name:
            custom_console.bot_log(
                "'No results found in IGDB with platform'\n\nTrying without platform:"
            )
            result = self._query(title=normalized_title, platform_name="")

        # If still no results, perform a broader search using a key term
        if not result:
            custom_console.bot_log(
                "'No results found in IGDB'\n\nTrying a broader search:"
            )
            result = self._query(title=normalized_title.split()[0], platform_name="")

        # Filter results to match the closest game name
        filtered_result = self._filter_results(result, normalized_title)
        finale_result = filtered_result if filtered_result else result

        # Print the results and ask the user for their choice
        user_select = self.select_result(results=finale_result) if len(finale_result) > 1 else 0
        return finale_result[user_select]

    def _query(self, title: str, platform_name: str) -> list["Game"]:
        header_access = {
            "Client-ID": config.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            # Filter by category to include main games, DLCs, remakes, remasters, expansions, and expanded games
            category_filter = "category = (0, 1, 2, 8, 9, 10)"
            if platform_name:
                query = f'fields id,name,summary; search "{title}"; where platforms = ({platform_name}) & {category_filter};'
            else:
                query = f'fields id,name,summary; search "{title}"; where {category_filter};'

            build_request = urljoin(base_request_url, "games")
            # custom_console.bot_log(f"IGDB Query: '{query}'") Debug

            response = self.http_client.get_url(
                build_request, get_method=False, headers=header_access, data=query
            )

            if response.status_code != 200:
                custom_console.bot_error_log(
                    f"Error from IGDB API: {response.status_code} - {response.text}"
                )
                return []

            try:
                query_result = response.json()
            except ValueError:
                custom_console.bot_error_log("Failed to parse JSON response.")
                return []

            if not query_result:
                return []

            return [Game(**game_data) for game_data in query_result]

        except Exception as e:
            custom_console.bot_error_log(
                f"Please report it {e} {self.__class__.__name__}"
            )
            exit(1)

    @staticmethod
    def _filter_results(games: list["Game"], search_title: str) -> list["Game"]:
        """
        Filters the list of games to find the closest match to the search title.
        """
        lower_search_title = search_title.lower()

        # Find games that have the closest match to the title
        matches = [game for game in games if lower_search_title in game.name.lower()]

        # If exact matches found, return them; otherwise, return partial matches
        if matches:
            return matches
        return games

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

        for index, result in enumerate(igdb_results):
            table.add_row(
                str(index),
                str(result.id),
                result.name,
                result.summary,
            )

        custom_console.bot_log(Align.center(table))

    # Ask user to choice a result
    def select_result(self, results: list["Game"]) -> None | int:

        # Print the results
        custom_console.bot_log("\nResults:")
        if results:
            self.view_results(igdb_results=results)
            while 1:
                result = self.input_manager()
                if result is not None and 0 <= result < len(results):
                    custom_console.bot_log(f"Selected: {result} -> {results[result].name}")
                    return result

    @staticmethod
    def input_manager() -> int | None:
        custom_console.print("\nChoice a result to send to the tracker (Q=exit) ", end='', style='violet bold')
        user_choice = input()
        if user_choice.upper() == "Q":
            exit(1)
        if user_choice.isdigit():
            return int(user_choice)
