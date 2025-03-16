# -*- coding: utf-8 -*-
import hashlib
import diskcache

from common.external_services.imageHost import Build
from common.mediainfo import MediaFile
from common.frames import VideoFrame

from view import custom_console
from unit3dup import config_settings


class Video:
    """ Build a description for the torrent page: screenshots, mediainfo, trailers, metadata """

    def __init__(self, file_name: str,  tmdb_id: int, trailer_key=None):
        self.file_name: str = file_name
        self.tmdb_id: int = tmdb_id
        self.trailer_key: int = trailer_key
        self.cache = diskcache.Cache(str(config_settings.user_preferences.CACHE_PATH))

        # Create a cache key for tmdb_id
        self.cache_key = self.hash_key(self.tmdb_id)

        # Load the video frames
        samples_n = max(2, min(config_settings.user_preferences.NUMBER_OF_SCREENSHOTS, 10))
        self.video_frames: VideoFrame = VideoFrame(self.file_name, num_screenshots=samples_n, tmdb_id=self.tmdb_id)

        # Init
        self.is_hd: int = 0
        self.description: str = ''
        self.mediainfo: str = ''

    @staticmethod
    def hash_key(tmdb_id) -> str:
        """ Generate a hashkey for the cache index """
        key_string = f"_{tmdb_id}"
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()

    def build_info(self):
        """Build the information to send to the tracker"""
        if config_settings.user_preferences.CACHE_SCR and self.tmdb_id > 0:
            description = self.cache.get(self.cache_key)
            if description:
                self.description = description.get('description', '')
                self.is_hd = description.get('is_hd', 0)

        if not self.description:
            # If no description found generate it
            custom_console.bot_log(f"\n[GENERATING IMAGES..] [HD {'ON' if self.is_hd == 0 else 'OFF'}]")
            extracted_frames, is_hd = self.video_frames.create()
            custom_console.bot_log("Done.")
            build_description = Build(extracted_frames=extracted_frames)
            self.description = build_description.description()
            self.description += (f"[b][spoiler=Spoiler: PLAY TRAILER][center][youtube]{self.trailer_key}[/youtube]"
                                 f"[/center][/spoiler][/b]")
            self.description += f"[url=https://github.com/31December99/Unit3Dup]Uploaded by Unit3Dup[/url]"
            self.is_hd = is_hd

        # Caching
        if config_settings.user_preferences.CACHE_SCR and self.tmdb_id > 0:
            self.cache[self.cache_key] = {'tmdb_id': self.tmdb_id, 'description': self.description, 'is_hd': self.is_hd}

        # media_info
        self.mediainfo = self._mediainfo()

    def _mediainfo(self) -> str:
        """Return media_info """
        media_info = MediaFile(self.file_name)
        return media_info.info
