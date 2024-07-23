# -*- coding: utf-8 -*-
import json


class Contents:

    def __init__(self, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int,
                 tracker_name: str, torrent_pack: bool):
        self.file_name = file_name
        self.name = name
        self.folder = folder
        self.size = size
        self.metainfo = metainfo
        self.category = category
        self.tracker_name = tracker_name
        self.torrent_pack = torrent_pack

    @classmethod
    def create_instance(cls, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int,
                        tracker_name: str, torrent_pack: bool):
        return cls(file_name, folder, name, size, metainfo, category, tracker_name, torrent_pack)
