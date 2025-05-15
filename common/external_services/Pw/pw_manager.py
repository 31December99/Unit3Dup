# -*- coding: utf-8 -*-

import argparse
import os

from common.external_services.Pw.pw_service import PwService
from common.utility import ManageTitles
from common.database import Database
from common import config_settings
from unit3dup.media import Media


from qbittorrent import Client
from view import custom_console

class PwManager:

    def __init__(self,cli: argparse.Namespace):
        # Keyword
        self.search = cli.pw

        # filename for the new download
        self.filename = ManageTitles.normalize_filename(self.search)

        # Select the tracker database
        self.database = Database(db_file=cli.tracker)


    def process(self):

        # a new qbittorrent instance
        qb = Client(f"http://{config_settings.torrent_client_config.QBIT_HOST}:{config_settings.torrent_client_config.QBIT_PORT}/")
        # a new pw instance
        pw_service = PwService()
        # Query the indexers
        search = pw_service.search(query=self.search)

        content = []
        if search:
            for index, s in enumerate(search):
                    if s.seeders > 0:
                        category = s.categories[0]['name']
                        if category in ['Movies','TV','TV/HD']:
                            content.append(s)
            custom_console.bot_process_table_pw(content=content)


            for c in content:
                test = Media(folder=f"c:\\test\\{c.fileName}", subfolder=f"c:\\test\\{c.fileName}")
                print(f"[Prowlarr] {c.fileName}")
                self.database.search(test.guess_title)


            """"
            qb.login(username=config_settings.torrent_client_config.QBIT_USER,
                     password=config_settings.torrent_client_config.QBIT_PASS)

            for torrent in content:
                filename = str(os.path.join(config_settings.options.PW_TORRENT_ARCHIVE_PATH,torrent.fileName))
                print(filename)
                magnet = pw_service.get_torrent_from_pw(torrent_url=torrent.downloadUrl,download_filename=filename)
                qb.download_from_link(magnet, savepath=config_settings.options.PW_DOWNLOAD_PATH)
            """
