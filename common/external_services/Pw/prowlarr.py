# -*- coding: utf-8 -*-
import os
import re

from common.external_services.Pw.pw_service import PwService
from common.utility import ManageTitles, System
from common.database import Database
from unit3dup.media import Media
from common import config_settings
from common.trackers.trackers import TRACKData
from common.page import Page



from qbittorrent import Client
from view import custom_console

class Prowlarr:

    def __init__(self):
        # a new instance for Prowalarr
        self.pw_service = PwService()
        # a new database instance
        self.database = Database(db_file='itt')
        self.tracker_data = TRACKData.load_from_module(tracker_name='itt')

    # Init http session
    async def init(self):
        await self.pw_service.init()

    @staticmethod
    async def get_season(pw_media: Media):
        if isinstance(pw_media.guess_episode, list):
            for episode in pw_media.guess_episode:
                print(f"E{str(episode).zfill(2)}")
        else:
            print(f"E{str(pw_media.guess_episode).zfill(2)}")

    async def search(self, web_query: str):

        qb = Client(
            f"http://{config_settings.torrent_client_config.QBIT_HOST}:{config_settings.torrent_client_config.QBIT_PORT}/")

        qb.login(username=config_settings.torrent_client_config.QBIT_USER,
                 password=config_settings.torrent_client_config.QBIT_PASS)

        # Query the indexers
        results = await self.pw_service.search(query=web_query)
        # return with no results
        if not results:
            return None

        # Filter based on movie and serie
        filtered_results = await self.filter(results=results)

        for f in filtered_results:
            print(f)
            await self.pw_service.get_page(url=f)


        input("END Press Enter to continue...")
        await self.pw_service.close()
        return

        custom_console.bot_process_table_pw(filtered_results)

        download_list = []
        for result, type_id, resolution in filtered_results:
            pw_media = Media(folder=f"c:\\test\\{result.fileName}", subfolder=f"c:\\test\\{result.fileName}")
            filename = str(os.path.join(config_settings.options.PW_TORRENT_ARCHIVE_PATH,result.fileName))
            search_in_db = await self.tracker_database(pw_media)
            if search_in_db:
                # ok !
                # qb.download_from_link(result.downloadUrl, savepath=config_settings.options.PW_DOWNLOAD_PATH)
                download_list.append(filename)
                custom_console.bot_log(f"Downloading {filename}")
        await self.pw_service.close()

        #TODO: confrontare i files in pw con quelli del database basandosi su
        # type_id , codec, risoluzione,bitrate
        return None


    @staticmethod
    async def resolution_from_title(title: str):
        screen_split = ManageTitles.clean_text(title).split(" ")
        for screen in screen_split:
            if screen in System.RESOLUTION_labels:
                return screen
        return None

    async def filter(self, results: list) -> list | None:

        content = []
        # Add an index and read results
        for index, s in enumerate(results):
            # with seeders
            if s.seeders > 0:
                content.append(s.infoUrl)
                category = s.categories[0]['name']
                # and categories
                if category in ['Movies', 'TV', 'TV/HD', 'Movies/HD', 'Movies/UHD']:
                    content.append([s, self.tracker_data.filter_type(s.fileName, return_tag=True),
                                    await self.resolution_from_title(s.fileName)])
        return content

    async def tracker_database(self, pw_media: Media)-> bool:
        db_search = self.database.search(pw_media.guess_title)

        if db_search:
            for filename in db_search:
                file_from_db = Media(folder=f"c:\\test\\{filename}", subfolder=f"c:\\test\\{filename}")
                if pw_media.category == 'serie':
                    # Regex per estrarre la stagione e l'episodio
                    pattern = r"S(\d{2})E(\d{2})"
                    torrent_pack = re.search(r"(S\d+(?!.*E\d+))|(S\d+E\d+-E?\d+)", filename)
                    if torrent_pack:
                        print(f"> {torrent_pack.groups()}")

                    match = re.search(pattern, filename)
                    if match:
                        season = match.group(1)
                        episode = match.group(2)
                        print(f"[DATABASE SERIE] {file_from_db.guess_title} - S{season.zfill(2)}E{episode.zfill(2)}")
                else:
                    print(f"[DATABASE MOVIE] {file_from_db.guess_title}")
            return True
        return False


