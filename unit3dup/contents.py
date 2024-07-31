import json
import os


class Contents:

    def __init__(
        self,
        file_name: str,
        folder: str,
        name: str,
        size: int,
        metainfo: json,
        category: int,
        tracker_name: str,
        torrent_pack: bool,
        torrent_path: str,
        display_name: str,
    ):
        self.file_name = file_name
        self.name = name
        self.folder = folder
        self.size = size
        self.metainfo = metainfo
        self.category = category
        self.tracker_name = tracker_name
        self.torrent_pack = torrent_pack
        self.torrent_path = torrent_path
        self.display_name = display_name

    @classmethod
    def create_instance(
        cls,
        file_name: str,
        folder: str,
        name: str,
        size: int,
        metainfo: json,
        category: int,
        tracker_name: str,
        torrent_pack: bool,
        torrent_path: str,
        display_name: str,
    ):
        return cls(
            file_name,
            folder,
            name,
            size,
            metainfo,
            category,
            tracker_name,
            torrent_pack,
            torrent_path,
            display_name,
        )


class File:
    """
    For each File , create an object with attributes:
    file_name, folder, media_type
    """

    def __init__(self, file_name: str, folder: str, media_type: str, torrent_name: str):
        self.torrent_path = os.path.join(folder, file_name)
        self.folder = folder
        self.media_type = media_type
        self.torrent_name = torrent_name

    @classmethod
    def create(cls, file_name: str, folder: str, media_type: str, torrent_name: str):
        return cls(file_name, folder, media_type, torrent_name)


class Folder:
    """
    For each Folder, create an object with attributes:
    folder, subfolder, media_type
    """

    def __init__(self, folder: str, subfolder: str, media_type: str, torrent_name: str):
        self.torrent_path = os.path.join(folder, subfolder)
        self.subfolder = subfolder
        self.media_type = media_type
        self.torrent_name = torrent_name

    @classmethod
    def create(cls, folder: str, subfolder: str, media_type: str, torrent_name: str):
        return cls(folder, subfolder, media_type, torrent_name)
