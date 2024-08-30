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
    - Upload screenshots to ImgBB
    - Return the video size
    - Determine if the video is standard definition (SD) or not
    """

    def __init__(self, file_name: str):

        self.IMGBB_KEY = config.IMGBB_KEY
        self.FREE_IMAGE_KEY = config.FREE_IMAGE_KEY

        self.file_name = file_name
        # Frame count
        self.numero_di_frame = None
        # Screenshots samples
        self.samples_n = config.SCREENSHOTS if 2 <= config.SCREENSHOTS <= 10 else 4
        # Catturo i frames del video
        # self.video_capture = cv2.VideoCapture(self.file_name)
        self.is_hd = False

    @property
    def fileName(self) -> str:
        return self.file_name

    @property
    def standard(self) -> int:
        """Determine if the video is standard definition (SD) or HD."""
        # is_hd = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT) >= 720
        console.log(f"[HD]........... {'YES' if self.is_hd else 'NO'}")
        return 0 if self.is_hd else 1

    @property
    def mediainfo(self) -> str:
        """Return media info as a string."""
        media_info = MediaFile(self.file_name)
        return media_info.info


    @property
    def frames(self) -> list:
        """
        Return a list of frames as byte arrays.
        """
        video_frames = VideoFrame(self.file_name, num_screenshots=self.samples_n)
        extract_screenshots = video_frames.create()
        self.is_hd = video_frames.is_hd

        return extract_screenshots

    @property
    def description(self) -> str:
        """Generate a description with image URLs uploaded to ImgBB"""
        console.log("\n[GENERATING IMAGES FROM VIDEO...]")
        description = "[center]\n"
        console_url = []

        for img_bytes in self.frames:

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
