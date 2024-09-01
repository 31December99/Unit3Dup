# -*- coding: utf-8 -*-

from typing import List, Optional
from unit3dup.files import Files
from unit3dup.automode import Auto


class ContentManager:
    def __init__(self, path: str, tracker_name: str, mode: str):
        self.path = path
        self.tracker_name = tracker_name
        self.mode = mode

    def get_files(self) -> List:
        return self.manual(self.mode) if self.mode in ["man", "folder"] else self.auto()

    def manual(self, mode: str) -> List:
        auto = Auto(path=self.path, mode=mode, tracker_name=self.tracker_name)
        return auto.upload()

    def auto(self) -> List:
        auto = Auto(path=self.path, tracker_name=self.tracker_name)
        return auto.scan()

    def get_media(self, item) -> Optional:
        files = Files(
            path=item.torrent_path,
            tracker_name=self.tracker_name,
            media_type=item.media_type,
        )
        content = files.get_data()
        if content is False:
            return None
        return content
