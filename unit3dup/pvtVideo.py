# -*- coding: utf-8 -*-
import diskcache

from common.external_services.imageHost import ImgBB, Freeimage, LensDump, ImageUploaderFallback, PtScreens, ImgFi,Build
from common.mediainfo import MediaFile
from common.frames import VideoFrame

from view import custom_console

from unit3dup import config_settings

offline_uploaders = []


class Video:
    """
    - Generate screenshots for each video provided
    - Obtain media info for each video and for the first video in a series
    - Upload screenshots and create a new description
    - Determine if the video is standard definition (SD) or not
    """

    def __init__(self, file_name: str,  tmdb_id: int, trailer_key = None):

        # Host APi keys
        self.IMGBB_KEY = config_settings.tracker_config.IMGBB_KEY
        self.FREE_IMAGE_KEY = config_settings.tracker_config.FREE_IMAGE_KEY
        self.LENSDUMP_KEY= config_settings.tracker_config.LENSDUMP_KEY
        self.PTSCREENS_KEY= config_settings.tracker_config.PTSCREENS_KEY
        self.IMGFI_KEY = config_settings.tracker_config.IMGFI_KEY

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

    def build_info(self):
        """Build the information to send to the tracker"""

        # If cache is enabled and the video is already cached
        # and if tmdb is not zero (tmdb ID not found) otherwise it will overwrite the same video in the cache
        if config_settings.user_preferences.CACHE_SCR and self.tmdb_id > 0:
            description = self.load_cache(self.tmdb_id)
            if isinstance(description, dict):
                self.description = description['description']
                self.is_hd = description['is_hd']
                if not self.description:
                    custom_console.bot_warning_log(f""
                                                   f"[{self.__class__.__name__}] The description in the cache is empty")
        else:
            self.description = None

        if not self.description:
            # If there is no cache available
            custom_console.bot_log(f"\n[GENERATING IMAGES..] [HD {'ON' if self.is_hd == 0 else 'OFF'}]")
            extracted_frames, is_hd = self.video_frames.create()
            custom_console.bot_log("Done.")
            build_description = Build(extracted_frames=extracted_frames)
            self.description = build_description.description()
            self.description += (f"[b][spoiler=Spoiler: PLAY TRAILER][center][youtube]"
                                 f"{self.trailer_key}[/youtube][/center][/spoiler][/b]")
            self.is_hd = is_hd

        # Write the new description to the cache
        if config_settings.user_preferences.CACHE_SCR and self.tmdb_id > 0:
            self.cache[self.tmdb_id] = {'description' : self.description, 'is_hd' : self.is_hd}
        # Create a new media info object
        self.mediainfo = self._mediainfo()


    def _mediainfo(self) -> str:
        """Return media info as a string."""
        media_info = MediaFile(self.file_name)
        return media_info.info


    def load_cache(self, index_: int):

        # Check if the item is in the cache
        if index_ not in self.cache:
            return False

        custom_console.bot_warning_log(f"** {self.__class__.__name__} **: Using cached Description!")

        try:
            # Try to get the video from the cache
            video = self.cache[index_]
        except KeyError:
            # Handle the case where the video is missing or the cache is corrupted
            custom_console.bot_error_log("Cached frame not found or cache file corrupted")
            custom_console.bot_error_log("Proceed to extract the screenshot again. Please wait..")
            return False

        # // OK
        return video
