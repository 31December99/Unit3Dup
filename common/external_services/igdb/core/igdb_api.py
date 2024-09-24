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
            "client_secret": config.IGDB_ACCESS_TK,
            "grant_type": "client_credentials",
        }

        if not config.IGDB_CLIENT_ID:
            custom_console.bot_question_log("No IGDB_CLIENT_ID provided\n")
            return False

        if not config.IGDB_ACCESS_TK:
            custom_console.bot_question_log("No IGDB_ACCESS_TK provided\n")
            return False

        response = cls.http_client.get_url(oauth, params=params, get_method=False)
        if response:
            authentication = response.json()
            cls.access_token = authentication["access_token"]
            cls.expires = authentication["expires_in"]
            cls.token_type = authentication["token_type"]
            return True
        else:
            return False

    def request(self, title: str, platform: list) -> list["Game"]:
        self.initialize_http_client()

        if not self.access_token:
            custom_console.bot_question_log("Login required. Please login first.\n")
            if not IGdbServiceApi.cls_login():
                custom_console.bot_question_log("Login failed.\n")
                return []

        # The platform name comes from the title
        if platform:
            if platform[0].upper() in platform_id:
                # The platform ID comes from the IGDB database
                platform_name = platform_id[platform[0].upper()]
            else:
                custom_console.bot_error_log(
                    f"Platform {platform} name not found in the BOT database "
                    f"for the title '{title}'\n"
                    f"Please report or add it"
                )
                exit(1)

        else:
            # Platform not found in content creation
            custom_console.bot_question_log(
                f"\nPlatform not found for the title '{title}'. Searching without it... \n"
            )
            platform_name = ""

        result = self._query(title=title, platform_name=platform_name)
        if not result and platform_name:
            result = self._query(title=title, platform_name="")
        return result

    def _query(self, title: str, platform_name: str) -> list["Game"]:

        header_access = {
            "Client-ID": config.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        try:
            if platform_name:
                query = f'fields id,name; search "{title}"; where platforms = ({platform_name});'
            else:
                query = f'fields id,name; search "{title}";'

            build_request = urljoin(base_request_url, "games")

            response = self.http_client.get_url(
                build_request, get_method=False, headers=header_access, data=query
            )

            query = response.json()
            return [Game(**game_data) for game_data in query]
        except Exception as e:
            custom_console.bot_error_log(f"Please report it {e}")
            exit(1)
