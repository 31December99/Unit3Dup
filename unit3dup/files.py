# -*- coding: utf-8 -*-
import json
import os
import re

from common.custom_console import custom_console
from common.utility.utility import Manage_titles
from common.trackers.trackers import ITTData
from unit3dup.contents import Contents
from common.mediainfo import MediaFile


class Files:
    """
    Identify the files (movies) and folders (series) regardless
    """

    def __init__(
            self,
            path: str,
            tracker_name: str,
            media_type: int,
            game_title: str,
            game_crew: list,
            game_tags: list,
    ):
        self.languages = None
        self.display_name = None

        # Contains the meta info for the torrent file
        self.meta_info_list: list = []

        self.meta_info = None
        self.size = None
        self.name = None
        self.folder = None
        self.file_name = None
        self.torrent_path = None
        self.doc_description = None

        self.category: int = media_type
        self.game_title: str = game_title
        self.game_crew: list = game_crew
        self.game_tags: list = game_tags
        self.tracker_name: str = tracker_name
        self.path: str = path
        self.movies: list = []
        self.series: list = []
        self.is_dir = os.path.isdir(self.path)
        self.tracker_data = ITTData.load_from_module()

    def get_data(self) -> Contents | bool:
        """
        Create an object with movie or series attributes for the torrent.
        Verify if name is part of torrent pack folder
        """
        if not self.is_dir:
            custom_console.bot_error_log(f"Process Files... <{self.path}>")
            # Check for valid extension
            process = (
                self.process_file() if Manage_titles.filter_ext(self.path) else False
            )
        else:
            custom_console.bot_error_log(f"Process Folder... <{self.path}>")
            process = self.process_folder()

        # Determines if it's a torrent pack by checking for a SxEx substring
        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))

        # If each file or folder has been processed correctly, we can create a unique content object
        # to make the torrent file, send it to the tracker...Start seeding
        return (
            Contents(
                file_name=self.file_name,
                folder=self.folder,
                name=self.name,
                size=self.size,
                metainfo=self.meta_info,
                category=self.category,
                tracker_name=self.tracker_name,
                torrent_pack=torrent_pack,
                torrent_path=self.torrent_path,
                display_name=self.display_name,
                doc_description=self.doc_description,
                audio_languages=self.languages,
                game_title=self.game_title,
                game_crew=self.game_crew,
                game_tags=self.game_tags,
            )
            if process
            else False
        )

    def process_file(self) -> bool:
        # The file determines the meta_info data
        self.file_name = os.path.basename(self.path)

        # Get the name of the folder in the path right before the file name
        # It is the user's responsibility to give the folder a meaningful name
        self.folder = os.path.dirname(self.path)

        # Contains the display_name, which is the name shown on the tracker page list
        # or on the tracker page
        self.display_name, ext = os.path.splitext(self.file_name)
        self.display_name = Manage_titles.clean(self.display_name)

        # Contains the path of the folder passed from the CLI command
        self.torrent_path = os.path.join(self.folder, self.file_name)

        # Description media_info inside the torrent page only for tv_show/movie categories
        media_info = MediaFile(file_path=os.path.join(self.folder, self.file_name))
        self.languages = media_info.available_languages

        # Field 'name' inside the torrent file. You can see it when downloading the torrent in the client
        self.name = self.file_name

        ###
        # Field description inside the torrent page for documents. not yet implemented
        self.doc_description = self.file_name
        media_docu_type = Manage_titles.media_docu_type(self.file_name)
        # If this is a document it becomes a document category
        if media_docu_type:
            # overwrite media_type # todo: 'cover image' not yet implemented
            self.category = self.tracker_data.category.get(media_docu_type)
        ###

        # Build the meta_info for the torrent file
        # there is only one file. self.path of the file
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps(
            [{"length": self.size, "path": [self.file_name]}], indent=4
        )
        return True

    def process_folder(self) -> bool:
        # Search for game files
        if self.category == self.tracker_data.category.get('game'):
            files_list = self.list_game_files()
        else:
            # Search for video files/docu ( not yet implemented)
            files_list = self.list_video_files()

        if not files_list:
            return False

        # The first file in list determines the meta_info data per the whole folder
        self.file_name = files_list[0]

        # Contains the path of the folder passed from the CLI command
        self.folder = self.path

        if self.category != self.tracker_data.category.get('game'):
            # Description media_info inside the torrent page only for tv_show/movie categories
            media_info = MediaFile(file_path=os.path.join(self.folder, self.file_name))
            self.languages = media_info.available_languages

        # Contains the display_name, which is the name shown on the tracker page list
        # or on the tracker page
        self.display_name = Manage_titles.clean(os.path.basename(self.path))

        # Contains the path of the folder passed from the CLI command
        self.torrent_path = self.folder

        # Field 'name' inside the torrent file. You can see it when downloading the torrent in the client
        self.name = os.path.basename(self.folder)

        ###
        # Field description inside the torrent page for documents. not yet implemented
        self.doc_description = "\n".join(files_list)
        media_docu_type = Manage_titles.media_docu_type(self.file_name)
        # If there is a document in the folder it becomes a document folder
        if media_docu_type:
            # overwrite media_type # todo: 'cover image' not yet implemented
            self.category = self.tracker_data.category.get(media_docu_type)
        ###

        # Build the meta_info for the torrent file
        total_size = 0
        for file in files_list:
            # get size of the file
            size = os.path.getsize(os.path.join(self.folder, file))
            # add the size and path of the current file
            self.meta_info_list.append({"length": size, "path": [file]})
            # Sum size for each file
            total_size += size

        # Get the total size
        self.size = total_size
        # create the json string for the meta_info and return
        self.meta_info = json.dumps(self.meta_info_list, indent=4)
        return True

    def list_video_files(self) -> list:
        """
        Add every video file to the list
        """
        return [
            file for file in os.listdir(self.path) if Manage_titles.filter_ext(file)
        ]

    def list_game_files(self) -> list:
        """
        Add every file to the list
        """
        return [file for file in os.listdir(self.path)]
