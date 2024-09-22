# -*- coding: utf-8 -*-
import pprint

from common.external_services.igdb.igdb_service import IGdbServiceApi
from common.external_services.igdb.core.models.game import Game
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.upload import UploadGame
from unit3dup.contents import Contents


class GameManager:

    def __init__(self, content: Contents):
        self.content = content
        self._my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        self._unit3d_up = UploadGame(content)
        # IGDB service
        self.ig_db = IGdbServiceApi()
        self.ig_db_data: list['Game'] = []

    def igdb(self):
        response = self.ig_db.login()
        if response:
            print(self.content.game_crew)
            self.ig_db_data = self.ig_db.request(self.content.game_title, platform=self.content.game_crew)
            print(self.ig_db_data)

    def torrent(self):
        self._my_torrent.hash()
        return self._my_torrent if self._my_torrent.write() else None

    def upload(self):
        # Create a new payload
        #todo : choose the best match not [0]
        data = self._unit3d_up.payload(igdb=self.ig_db_data[0])

        # Get a new tracker instance
        tracker = self._unit3d_up.tracker(data=data)

        # Send the payload
        return self._unit3d_up.send(tracker=tracker)
