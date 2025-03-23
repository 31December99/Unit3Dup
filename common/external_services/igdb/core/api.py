# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from common.external_services.sessions.session import MyHttp
from common import config_settings
from view import custom_console

class IGDBapi:

    params = {
        "client_id": config_settings.tracker_config.IGDB_CLIENT_ID,
        "client_secret": config_settings.tracker_config.IGDB_ID_SECRET,
        "grant_type": "client_credentials",
    }

    base_request_url = "https://api.igdb.com/v4/"
    oauth = "https://id.twitch.tv/oauth2/token"

    def __init__(self):
        self.access_header = None
        self.header_access = None
        self.http_client = None


    def login(self)-> bool:
        if not config_settings.tracker_config.IGDB_CLIENT_ID:
            custom_console.bot_question_log("No IGDB_CLIENT_ID provided\n")
            return False

        if not config_settings.tracker_config.IGDB_ID_SECRET:
            custom_console.bot_question_log("No IGDB_ID_SECRET provided\n")
            return False

        self.http_client = MyHttp({
            "User-Agent": "Unit3D-up/0.0 (Linux 5.10.0-23-amd64)",
            "Accept": "application/json",
        })


        response = self.http_client.post(self.oauth, params = {
            "client_id": config_settings.tracker_config.IGDB_CLIENT_ID,
            "client_secret": config_settings.tracker_config.IGDB_ID_SECRET,
            "grant_type": "client_credentials",
        })

        if response:
            authentication = response.json()
            access_token = authentication["access_token"]
            expires = authentication["expires_in"]
            token_type = authentication["token_type"]
            custom_console.bot_log("IGDB Login successful!")

            self.access_header = {
                "Client-ID": config_settings.tracker_config.IGDB_CLIENT_ID,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            return True
        else:
            custom_console.bot_error_log("Failed to authenticate with IGDB.\n")
            custom_console.bot_error_log("IGDB Login failed. Please check your credentials")
            return False


    def request(self, query:str , endpoint:str)-> list:
        build_request = urljoin(self.base_request_url, endpoint)
        response = self.http_client.post(build_request, headers=self.access_header, data=query)
        if response:
            return response.json()