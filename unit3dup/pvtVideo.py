# -*- coding: utf-8 -*-

from common.external_services.imageHost import ImgBB, Freeimage, ImageUploaderFallback
from common.mediainfo import MediaFile
from rich.console import Console
from common.config import config
from unit3dup.ping import offline_uploaders
from common.utility.frames import VideoFrame

console = Console(log_path=False)


class Video:
    """
    - Generate screenshots for each video provided
    - Obtain media info for each video and for the first video in a series
    - Upload screenshots and create a new description
    - Determine if the video is standard definition (SD) or not
    """

    def __init__(self, file_name: str):

        # Host APi keys
        self.IMGBB_KEY = config.IMGBB_KEY
        self.FREE_IMAGE_KEY = config.FREE_IMAGE_KEY

        # File name
        self.file_name: str = file_name

        # Screenshots samples
        samples_n: int = config.SCREENSHOTS if 2 <= config.SCREENSHOTS <= 10 else 4

        # New object frame
        self.video_frames: VideoFrame = VideoFrame(self.file_name, num_screenshots=samples_n)

        # Is_hd
        self.is_hd: int = 0

        # Description
        self.description: str = ''

        # Description
        self.mediainfo: str = ''

    @classmethod
    def info(cls, file_name: str):
        """
        Class method to create a new Video object from a file
        """
        # Create a new instance of the class
        video_instance = cls(file_name)

        # Call build_info
        video_instance._build_info()

        # Return a new instance
        return video_instance

    def _build_info(self):
        """ Build the info to send to the tracker"""

        # Return a list of frames and the hd info
        extracted_frames, is_hd = self.video_frames.create()
        self.is_hd = is_hd

        # Create a new description
        self.description = self._description(extracted_frames=extracted_frames)

        # Create a new mediainfo object
        self.mediainfo = self._mediainfo()

    def _mediainfo(self) -> str:
        """Return media info as a string."""
        media_info = MediaFile(self.file_name)
        return media_info.info

    def _description(self, extracted_frames: list) -> str:
        """Generate a description with image URLs uploaded to ImgBB"""
        console.log(f"\n[GENERATING IMAGES..] [HD {'ON' if self.is_hd==0 else 'OFF'}]")
        description = "[center]\n"
        console_url = []
        for img_bytes in extracted_frames:

            master_uploaders = [
                Freeimage(img_bytes, self.FREE_IMAGE_KEY),
                ImgBB(img_bytes, self.IMGBB_KEY),
            ]

            # for each on-line uploader
            for uploader in master_uploaders:
                if not uploader.__class__.__name__ in offline_uploaders:
                    # Upload the screenshot
                    fallback_uploader = ImageUploaderFallback(uploader)
                    # Get a new URL
                    img_url = fallback_uploader.upload()

                    # If it goes offline during upload skip the uploader
                    if not img_url:
                        console.log(
                            "** Upload failed, skip to next host **", style="red bold"
                        )
                        offline_uploaders.append(uploader.__class__.__name__)
                        continue
                    console.log(img_url)
                    # Append the URL to new description
                    console_url.append(img_url)
                    description += f"[url={img_url}][img=350]{img_url}[/img][/url]"
                    # Got description for this screenshot
                    break

        # Append the new URL to the description string
        description += "\n[/center]"
        return description
