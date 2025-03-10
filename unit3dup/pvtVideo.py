# -*- coding: utf-8 -*-
import hashlib
import diskcache

from common.external_services.imageHost import Build
from common.mediainfo import MediaFile
from common.frames import VideoFrame

from view import custom_console
from unit3dup import config_settings

offline_uploaders = []


class Video:
    """
    - Get screenshots for each provided video
    - Obtain media info for each video and for the first video in a series
    - Upload screenshots and create a new description
    - Determine if the video is standard definition (SD) or not
    """

    def __init__(self, file_name: str,  tmdb_id: int, trailer_key = None):

        # File name
        self.file_name: str = file_name

        # YouTube trailer key
        self.trailer_key: int = trailer_key

        # Screenshots samples
        samples_n: int = config_settings.user_preferences.NUMBER_OF_SCREENSHOTS\
            if 2 <= config_settings.user_preferences.NUMBER_OF_SCREENSHOTS <= 10 else 4

        # New object frame
        self.video_frames: VideoFrame = VideoFrame(self.file_name, num_screenshots=samples_n, tmdb_id=tmdb_id)

        # Is_hd
        self.is_hd: int = 0

        # Description
        self.description: str = ''

        # Description
        self.mediainfo: str = ''

        # For frame caching
        self.tmdb_id = tmdb_id

        # description cache
        self.cache = diskcache.Cache(str(config_settings.user_preferences.CACHE_PATH))

        # Create the hask key for the cache index
        self.cache_key = self.hash_key(self.tmdb_id)

        # Load the description using hash_key and if tmdb_id > 0 (0 = tmdb ID not found)
        self.description = self.cache.get(self.cache_key) if (self.cache.get(self.cache_key, None)
                                                              and self.tmdb_id > 0) else None

        import pprint
        pprint.pprint(self.description)

    @staticmethod
    def hash_key(tmdb_id) -> str:
        """ Generate an hashkey for the cache index """

        key_string = f"_{tmdb_id}"
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()

    def build_info(self):
        """Build the information to send to the tracker"""

        if not self.description:
            # If there is no cache available
            custom_console.bot_log(f"\n[GENERATING IMAGES..] [HD {'ON' if self.is_hd == 0 else 'OFF'}]")
            extracted_frames, is_hd = self.video_frames.create()
            custom_console.bot_log("Done.")
            build_description = Build(extracted_frames=extracted_frames)
            self.description = build_description.description()
            self.description += (f"[b][spoiler=Spoiler: PLAY TRAILER][center][youtube]"
                                 f"{self.trailer_key}[/youtube][/center][/spoiler][/b]"
                                 f"[url=https://github.com/31December99/Unit3Dup]By Unit3Dup[/url]")
            self.is_hd = is_hd

        if config_settings.user_preferences.CACHE_SCR and self.tmdb_id > 0:
            self.cache[self.cache_key] = {'tmdb_id': self.tmdb_id,'description': self.description,'is_hd': self.is_hd}

        # Create a new media info object
        self.mediainfo = self._mediainfo()


    def _mediainfo(self) -> str:
        """Return media info as a string."""
        media_info = MediaFile(self.file_name)
        return media_info.info
