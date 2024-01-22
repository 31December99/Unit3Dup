# -*- coding: utf-8 -*-
import json


class Contents:

    def __init__(self, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int, tracker_name: str):
        self.file_name = file_name
        self.name = name
        self.folder = folder
        self.size = size
        self.metainfo = metainfo
        self.category = category
        self.tracker_name = tracker_name

    @classmethod
    def create_instance(cls, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int,
                        tracker_name: str):
        return cls(file_name, folder, name, size, metainfo, category, tracker_name)
