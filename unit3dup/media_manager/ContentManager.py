# -*- coding: utf-8 -*-
import multiprocessing

from unit3dup.contents import Contents
from unit3dup.contents import Media
from unit3dup.automode import Auto
from unit3dup.files import Files
from common.custom_console import custom_console

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

    def get_files(self) -> list['Contents']:
        """Based on selected mode"""
        if self.mode in ["man", "folder"]:
            # Manual call to load files from specified path
            auto = Auto(path=self.path, mode=self.mode, tracker_name=self.tracker_name,force_media_type=self.force_media_type)
            # run cli flag
            file_list = auto.upload()
            return self.process(file_list=file_list)
        else:
            # Automatic call to load files based on detected content..
            auto = Auto(path=self.path, tracker_name=self.tracker_name, force_media_type=self.force_media_type)
            # run cli flag
            file_list = auto.scan()
            return self.process(file_list=file_list)


    def process(self, file_list: list['Media']) -> list['Contents']:
        """ process media files and return 'contents' """

        contents = []
        try:
            with multiprocessing.Pool(processes=4) as pool:
                contents = pool.map(self.create_content_from_media, file_list)
        except KeyboardInterrupt:
            # Try to clean...
            custom_console.bot_error_log("Interrupted by the user. Exiting...")
            pool.terminate()
            pool.join()
            custom_console.bot_warning_log("Processes ended")
        except Exception as e:
            custom_console.bot_error_log(f"Error: {e}. Please report it")
            pool.terminate()
            pool.join()
        finally:
            return contents


    def create_content_from_media(self, media: 'Media') -> Contents:
        """Creates a `Contents` object for each media item"""
        # Create content using the file or folder specified by the media object
        files = Files(
            path=media.torrent_path,
            tracker_name=self.tracker_name,
            guess_title = media.guess_title,
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
