# -*- coding: utf-8 -*-

from typing import List, Optional
from unit3dup.files import Files
from unit3dup.automode import Auto


class ContentManager:
    def __init__(self, path: str, tracker_name: str, mode: str, force_media_type = None):
        self.path = path
        self.tracker_name = tracker_name
        self.mode = mode
        self.force_media_type = force_media_type

    def get_files(self) -> List:
        # Create a list of file objects (Media) based on the commands from the CLI user
        # For each media object, add basic attributes from the create_path method of the AutoMode class
        return self.manual(self.mode) if self.mode in ["man", "folder"] else self.auto()

    def manual(self, mode: str) -> List:
        auto = Auto(path=self.path, mode=mode, tracker_name=self.tracker_name, force_media_type=self.force_media_type)
        return auto.upload()

    def auto(self) -> List:
        auto = Auto(path=self.path, tracker_name=self.tracker_name, force_media_type=self.force_media_type)
        return auto.scan()

    def get_media(self, item) -> Optional:
        # Create a Files object with basic information from the Media class
        # and obtain the content object by adding more attributes
        files = Files(
            path=item.torrent_path,
            tracker_name=self.tracker_name,
            media_type=item.media_type,
            game_title=item.game_title,
            game_crew=item.crew,
            game_tags=item.game_tags,
            season=item.guess_season,
            episode=item.guess_episode,
            screen_size=item.screen_size,
        )

        # Create and return a content object
        content = files.get_data()
        if content is False:
            return None
        return content
