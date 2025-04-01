# -*- coding: utf-8 -*-
import hashlib
import os.path

import diskcache

from common.external_services.imageHost import Build
from common.mediainfo import MediaFile
from common.frames import VideoFrame

from view import custom_console
from unit3dup import config_settings
from unit3dup.media import Media


class Video:
    """ Build a description for the torrent page: screenshots, mediainfo, trailers, metadata """

    def __init__(self, media: Media,  tmdb_id: int, trailer_key=None):
        self.file_name: str = media.file_name
        self.display_name: str = media.display_name

        self.tmdb_id: int = tmdb_id
        self.trailer_key: int = trailer_key
        self.cache = diskcache.Cache(str(config_settings.user_preferences.CACHE_PATH))

        # Create a cache key for tmdb_id
        self.key = f"{self.tmdb_id}.{self.display_name}"
        self.cache_key = self.hash_key(self.key)

        # Load the video frames
        samples_n = max(2, min(config_settings.user_preferences.NUMBER_OF_SCREENSHOTS, 10))
        self.video_frames: VideoFrame = VideoFrame(self.file_name, num_screenshots=samples_n)

        # Init
        self.is_hd: int = 0
        self.description: str = ''
        self.mediainfo: str = ''

    @staticmethod
    def hash_key(key: str) -> str:
        """ Generate a hashkey for the cache index """
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def build_info(self):
        """Build the information to send to the tracker"""
        if config_settings.user_preferences.CACHE_SCR:
            description = self.cache.get(self.cache_key)
            if description:
                custom_console.bot_warning_log(f"\n<> Using cached images for '{self.key}'")
                self.description = description.get('description', '')
                self.is_hd = description.get('is_hd', 0)

        if not self.description:
            # If no description found generate it
            custom_console.bot_log(f"\n[GENERATING IMAGES..] [HD {'ON' if self.is_hd == 0 else 'OFF'}]")
            # Extract the frames
            extracted_frames, is_hd = self.video_frames.create()
            # Create a webp file
            extracted_frames_webp = self.video_frames.create_webp_from_video(video_path=self.file_name,
                                                start_time=90,
                                                duration=10,
                                                output_path=
                                                os.path.join(config_settings.user_preferences.CACHE_PATH,"file.webp"))
            custom_console.bot_log("Done.")

            # Build the description
            build_description = Build(extracted_frames=extracted_frames_webp+extracted_frames, filename = self.file_name)
            self.description = build_description.description()
            self.description += (f"[b][spoiler=Spoiler: PLAY TRAILER][center][youtube]{self.trailer_key}[/youtube]"
                                 f"[/center][/spoiler][/b]")
            self.description += f"[url=https://github.com/31December99/Unit3Dup]Uploaded by Unit3Dup[/url]"
            self.is_hd = is_hd

        # Caching
        if config_settings.user_preferences.CACHE_SCR:
            self.cache[self.cache_key] = {'tmdb_id': self.tmdb_id, 'description': self.description, 'is_hd': self.is_hd}

        # media_info
        self.mediainfo = self._mediainfo()

    def _mediainfo(self) -> str:
        """Return media_info """
        media_info = MediaFile(self.file_name)
        return media_info.info
