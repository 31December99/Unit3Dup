import aiohttp

from common.trackers.trackers import TRACKData
from common.bittorrent import BittorrentData

from unit3dup.pvtTracker import Unit3d
from unit3dup import config_settings, Load

from abc import ABC, abstractmethod
from view import custom_console



class UploadBot(ABC):
    def __init__(self, torrent: BittorrentData):

        self.API_TOKEN = config_settings.tracker_config.ITT_APIKEY
        self.BASE_URL = config_settings.tracker_config.ITT_URL
        self.torrent = torrent
        self.cli = torrent.payload.cli
        self.content = torrent.content
        self.tracker_name = torrent.payload.tracker_name
        self.tracker_data = TRACKData.load_from_module(tracker_name=torrent.payload.tracker_name)
        self.sign = (f"[url=https://github.com/31December99/Unit3Dup][code][color=#00BFFF][size=14]Uploaded with Unit3Dup"
                     f" {Load.version}[/size][/color][/code][/url]")


    async def message(self, tracker_response: dict) -> (dict, dict):

        success = tracker_response.get('success', False)
        data = tracker_response.get('data', {})
        message = tracker_response.get('message', '')

        custom_console.bot_log(f"\n[RESPONSE]-> '{self.tracker_name}'.....{self.torrent.content.display_name} "
                               f"{message.upper()}\n")

        return data, {}

    async def _send(self, torrent_archive: str, data: dict, nfo_path = None) -> (aiohttp.ClientResponse, dict):
        async with Unit3d(tracker_name=self.torrent.payload.tracker_name) as tracker:
            tracker_response = await tracker.upload_t(data=data, torrent_archive_path = torrent_archive,nfo_path=nfo_path)
            response = await self.message(tracker_response)
        return response


    @abstractmethod
    def send(self, torrent_archive: str, nfo_path = None) -> (aiohttp.ClientResponse, dict):
        pass


class Show(UploadBot):
    async def send(self, path: str, nfo_path = None) -> (aiohttp.ClientResponse, dict):

        data = {}
        data["name"] = self.content.display_name
        data["tmdb"] = self.torrent.payload.show_id
        data["imdb"] = self.torrent.payload.imdb_id if self.torrent.payload.imdb_id else 0
        data["keywords"] = self.torrent.payload.show_keywords
        data["category_id"] = self.tracker_data.category.get(self.content.category)
        data["anonymous"] = int(config_settings.user_preferences.ANON)
        data["resolution_id"] = self.tracker_data.resolution[self.content.screen_size] \
            if self.content.screen_size else self.tracker_data.resolution[self.content.resolution]
        data["mediainfo"] = self.torrent.payload.video_info.mediainfo
        data["description"] = self.torrent.payload.video_info.description + self.sign
        data["sd"] = self.torrent.payload.video_info.is_hd
        data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        data["season_number"] = self.content.guess_season
        data["episode_number"] = (self.content.guess_episode if not self.content.torrent_pack else 0)
        data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                 or int(self.cli.personal))
        return await self._send(torrent_archive=path,data=data)

class Games(UploadBot):
    async def send(self, path: str, nfo_path=None) -> (aiohttp.ClientResponse, dict):

        igdb_platform = self.content.platform_list[0].lower() if self.content.platform_list else ''
        data = {}
        data["name"] = self.content.display_name
        data["tmdb"] = 0
        data["category_id"] = self.tracker_data.category.get(self.content.category)
        data["anonymous"] = int(config_settings.user_preferences.ANON)
        data["description"] = self.torrent.payload.igdb.description + self.sign if self.torrent.payload.igdb else "Sorry, there is no valid IGDB"
        data["type_id"] = self.tracker_data.type_id.get(igdb_platform) if igdb_platform else 1
        data["igdb"] = self.torrent.payload.igdb.id if self.torrent.payload.igdb else 1,  # need zero not one ( fix tracker)
        data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                             or int(self.cli.personal))
        return await self._send(torrent_archive=path, data=data, nfo_path=nfo_path)


class Doc(UploadBot):
    async def send(self, path: str, nfo_path=None) -> (aiohttp.ClientResponse, dict):

        data = {}
        data["name"] = self.content.display_name
        data["tmdb"] = 0
        data["category_id"] = self.tracker_data.category.get(self.content.category)
        data["anonymous"] = int(config_settings.user_preferences.ANON)
        data["description"] = self.torrent.payload.docu_info.description + self.sign
        data["type_id"] = self.tracker_data.filter_type(self.content.file_name)
        data["resolution_id"] = ""
        data["personal_release"] = (int(config_settings.user_preferences.PERSONAL_RELEASE)
                                                     or int(self.cli.personal))
        return await self._send(torrent_archive=path,data=data)