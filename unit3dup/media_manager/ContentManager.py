# -*- coding: utf-8 -*-

from unit3dup.contents import Contents
from unit3dup.contents import Media
from unit3dup.automode import Auto
from unit3dup.files import Files

from multiprocessing import Pool


class ContentManager:
    def __init__(self, path: str, tracker_name: str, mode: str, force_media_type=None):
        """
        Args:
            path (str): The path to the media files or directories
            tracker_name (str): The tracker name for the content
            mode (str):  mode 'manual' or 'automatic'
            force_media_type: if the -serie, -movie, -game si active
        """
        self.path = path
        self.tracker_name = tracker_name
        self.mode = mode
        self.force_media_type = force_media_type

    def get_files(self) -> list['Media']:
        """Based on selected mode"""
        if self.mode in ["man", "folder"]:
            # Manual call to load files from specified path
            return self.manual(self.mode)
        else:
            # Automatic call to load files based on detected content..
            return self.auto()

    def manual(self, mode: str) -> list['Media']:
        """Manual process """
        auto = Auto(path=self.path, mode=mode, tracker_name=self.tracker_name, force_media_type=self.force_media_type)
        file_list = auto.upload()

        # Get content object for each file
        with Pool(processes=4) as pool:
            contents = pool.map(self.create_content_from_media, file_list)

        return contents

    def auto(self) -> list['Media']:
        """Automatic process"""
        auto = Auto(path=self.path, tracker_name=self.tracker_name, force_media_type=self.force_media_type)
        file_list = auto.scan()

        # Get content object for each file
        with Pool(processes=4) as pool:
            contents = pool.map(self.create_content_from_media, file_list)

        return contents

    def create_content_from_media(self, media: 'Media') -> Contents:
        """Creates a `Contents` object for each media item"""
        # Create content using the file or folder specified by the media object
        files = Files(
            path=media.torrent_path,
            tracker_name=self.tracker_name,
            media_type=media.media_type,
            game_title=media.game_title,
            game_crew=media.crew,
            game_tags=media.game_tags,
            season=media.guess_season,
            episode=media.guess_episode,
            screen_size=media.screen_size,
        )

        # Get content data and return if valid
        content = files.get_data()
        return content if content else None
