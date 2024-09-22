# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from common.custom_console import custom_console
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common.external_services.igdb.core.models.game import Game
from common.external_services.igdb.core.platformid import platform_id
from common.config import config

base_request_url = "https://api.igdb.com/v4/"
oauth = "https://id.twitch.tv/oauth2/token"


class IGdbServiceApi(MyHttp):
    def __init__(self):
        self.headers = Agent.headers()
        self.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        super().__init__(self.headers)

        self.token_type: str = ""
        self.expires: str = ""
        self.access_token: str = ""

    def login(self) -> bool:
        params = {
            "client_id": config.IGDB_CLIENT_ID,
            "client_secret": config.IGDB_ACCESS_TK,
            "grant_type": "client_credentials",
        }

        if not config.IGDB_CLIENT_ID:
            custom_console.bot_question_log("No IGDB_CLIENT_ID provided\n")
            return False

        if not config.IGDB_ACCESS_TK:
            custom_console.bot_question_log("No IGDB_ACCESS_TK provided\n")
            return False

        # Login
        response = self.get_url(oauth, params=params, get_method=False)
        if response:
            authentication = response.json()
            # Get the access token
            self.access_token = authentication["access_token"]
            self.expires = authentication["expires_in"]
            self.token_type = authentication["token_type"]
            return True
        else:
            return False

    def request(self, title: str, platform: list) -> list["Game"]:

        header_access = {
            "Client-ID": config.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        # Search by title and platform
        query = f'fields id,name; search "{title}"; where platforms = ({platform_id[platform[0]]});'
        build_request = urljoin(base_request_url, "games")
        response = self.get_url(
            build_request, get_method=False, headers=header_access, data=query
        )
        query = response.json()
        return [Game(**game_data) for game_data in query]
