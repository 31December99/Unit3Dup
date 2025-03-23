# -*- coding: utf-8 -*-

import argparse
import os

from common.external_services.Pw.pw_service import PwService
from common.utility import ManageTitles
from common import config_settings

from qbittorrent import Client
from view import custom_console

class PwManager:

    def __init__(self,cli: argparse.Namespace):
        # Keyword
        self.search = cli.pw

        # filename for the new download
        self.filename = ManageTitles.normalize_filename(self.search)


    def process(self):

        # a new qbittorent instance
        qb = Client(f"http://{config_settings.tracker_config.QBIT_HOST}:{config_settings.tracker_config.QBIT_PORT}/")
        # a new pw instance
        pw_service = PwService()
        # Query the indexers
        search = pw_service.search(query=self.search)

        if search:
            for index, s in enumerate(search):
                if s.seeders > 0:
                    torrent_file = search[index]
                    custom_console.log(torrent_file.downloadUrl)
                    pw_service.get_torrent_from_pw(torrent_url=torrent_file.downloadUrl,download_filename=self.filename)

                    qb.login(username=config_settings.tracker_config.QBIT_USER,
                             password=config_settings.tracker_config.QBIT_PASS)

                    qb.download_from_file(
                        file_buffer=open(os.path.join(config_settings.options.PW_TORRENT_ARCHIVE_PATH,
                                                      f"{self.filename}.torrent"), "rb"),
                        savepath=config_settings.options.PW_DOWNLOAD_PATH,
                    )
