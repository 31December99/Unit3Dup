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
            doc_description: str,
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
        self.doc_description = doc_description

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
            doc_description: str,
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
            doc_description,
        )


class File:
    """
    For each File , create an object with attributes:
    file_name, folder, media_type
    """

    def __init__(self, file_name: str, folder: str, media_type: str, torrent_name: str, source: str, other: str,
                 audio_codec: str, subtitle: str, resolution: str ): # , torrent_path: str):
        self.folder = folder
        self.media_type = media_type
        self.torrent_name = torrent_name
        self.source = source
        self.other = other
        self.audio_code = audio_codec
        self.subtitle = subtitle
        self.resolution = resolution
        # self.torrent_path = torrent_path  # os.path.join(folder, file_name)

    @classmethod
    def create(cls, file_name: str, folder: str, media_type: str, torrent_name: str, source: str, other: str,
               audio_codec: str,
               subtitle: str, resolution: str):
        return cls(file_name, folder, media_type, torrent_name, source, other, audio_codec, subtitle, resolution)


class Folder:
    """
    For each Folder, create an object with attributes:
    folder, subfolder, media_type
    """

    def __init__(self, folder: str, subfolder: str, media_type: str, torrent_name: str, source: str, other: str,
                 audio_codec: str, subtitle: str, resolution: str):
        self.torrent_path = os.path.join(folder, subfolder)
        self.subfolder = subfolder
        self.media_type = media_type
        self.torrent_name = torrent_name
        self.source = source
        self.other = other
        self.audio_code = audio_codec
        self.subtitle = subtitle
        self.resolution = resolution

    @classmethod
    def create(cls, folder: str, subfolder: str, media_type: str, torrent_name: str, source: str,
               other: str, audio_codec: str, subtitle: str, resolution: str):
        return cls(folder, subfolder, media_type, torrent_name, source, other, audio_codec, subtitle,
                   resolution)
