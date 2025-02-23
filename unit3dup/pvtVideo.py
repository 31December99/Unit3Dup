# -*- coding: utf-8 -*-
import diskcache

from common.external_services.imageHost import ImgBB, Freeimage, LensDump, ImageUploaderFallback, PtScreens
from common.mediainfo import MediaFile
from common.frames import VideoFrame
from common.custom_console import custom_console

from unit3dup import config

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
        self.IMGBB_KEY = config.IMGBB_KEY
        self.FREE_IMAGE_KEY = config.FREE_IMAGE_KEY
        self.LENSDUMP_KEY= config.LENSDUMP_KEY
        self.PTSCREENS_KEY= config.PTSCREENS_KEY

        # File name
        self.file_name: str = file_name

        # YouTube trailer key
        self.trailer_key: int = trailer_key

        # Screenshots samples
        samples_n: int = config.NUMBER_OF_SCREENSHOTS if 2 <= config.NUMBER_OF_SCREENSHOTS <= 10 else 4

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
        self.cache = diskcache.Cache(str(config.default_env_path_cache))

    def build_info(self):
        """Build the information to send to the tracker"""

        # If cache is enabled and the video is already cached
        if config.CACHE_SCR:
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
            # Create a new description
            self.description = self._description(extracted_frames=extracted_frames)
            self.description += (f"[b][spoiler=Spoiler: PLAY TRAILER][center][youtube]"
                                 f"{self.trailer_key}[/youtube][/center][/spoiler][/b]")
            self.is_hd = is_hd


        # Write the new description to the cache
        if config.CACHE_SCR:
            self.cache[self.tmdb_id] = {'description' : self.description, 'is_hd' : self.is_hd}


        # Create a new media info object
        self.mediainfo = self._mediainfo()


    def _mediainfo(self) -> str:
        """Return media info as a string."""
        media_info = MediaFile(self.file_name)
        return media_info.info

    def _description(self, extracted_frames: list) -> str:
        """Generate a description with image URLs uploaded to ImgBB"""
        description = "[center]\n"
        console_url = []

        custom_console.bot_log("Starting image upload..")
        for img_bytes in extracted_frames:

            master_uploaders = [
                ImgBB(img_bytes, self.IMGBB_KEY),
                Freeimage(img_bytes, self.FREE_IMAGE_KEY),
                PtScreens(img_bytes, self.PTSCREENS_KEY),
                LensDump(img_bytes, self.LENSDUMP_KEY),
            ]

            # Sorting list based on priority
            master_uploaders.sort(key=lambda uploader: uploader.priority)

            # for each on-line uploader
            for uploader in master_uploaders:
                if not uploader.__class__.__name__ in offline_uploaders:
                    # Upload the screenshot
                    fallback_uploader = ImageUploaderFallback(uploader)
                    # Get a new URL
                    img_url = fallback_uploader.upload()

                    # If it goes offline during upload skip the uploader
                    if not img_url:
                        custom_console.bot_error_log(
                            "** Upload failed, skip to next host **"
                        )
                        offline_uploaders.append(uploader.__class__.__name__)
                        continue
                    custom_console.bot_log(img_url)
                    # Append the URL to new description
                    console_url.append(img_url)
                    description += f"[url={img_url}][img=650]{img_url}[/img][/url]"
                    # Got description for this screenshot
                    break

        # Append the new URL to the description string
        description += "\n[/center]"
        return description

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
