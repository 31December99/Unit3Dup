# -*- coding: utf-8 -*-


from common.external_services.igdb.core.igdb_api import IGdbServiceApi
from common.external_services.igdb.core.models.game import Game


class Igdb:
    """
    Igdb class to interact with the IGDB API for searching games and retrieving trailers

    Methods:
        login() -> bool: Logs into the IGDB API service.
        search(title: str, platform: list) -> Game: Searches for a game by title and trailers
        trailers(videos_id: list) -> str: Get the youtube trailers id
    """

    def __init__(self):
        """
        Initializes the IGDB API

        Args:
            None
        """
        self.ig_dbapi = IGdbServiceApi()

    def login(self) -> bool:
        """
        Logs into the IGDB API service

        Returns:
            bool: True if login is successful
        """
        return self.ig_dbapi.cls_login()

    def search(self, title: str, platform: list) -> Game:
        """
        Searches for a game by title and platform
        Add to Game object the full description ( summary + trailers)

        Args:
            title (str): The title of the game
            platform (list): A list of platforms from the Content media object

        Returns:
            Game: A Game object containing game details, description, and trailers.
        """
        game_data_results = self.ig_dbapi.request(title=title, platform=platform)

        description = game_data_results.summary
        description += "\n\n"
        description += self.trailers(game_data_results.videos)

        game_data_results.description = description

        return game_data_results

    def trailers(self, videos_id: list) -> str:
        """
        Get the youtube trailers string for a game based on the provided video id

        Args:
            videos_id (list): A list of video IDs to retrieve trailers for

        Returns:
            str: A string containing the formatted trailers in BBCode format or a warning message
        """
        if not videos_id:
            return "\nNo trailers available.\n"

        trailer_id_list = self.ig_dbapi.get_videos_id(videos_id)

        bbcode = "[b]Game Trailers:[/b]\n"
        for video_id in trailer_id_list:
            bbcode += (f"\n[b][spoiler=Spoiler: PLAY GAME TRAILER][center][youtube]{video_id}"
                        f"[/youtube][/center][/spoiler][/b]\n")
        return bbcode
