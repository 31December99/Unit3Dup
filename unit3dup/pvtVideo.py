# -*- coding: utf-8 -*-
import random
import cv2
from common.imageHost import ImgBB, Freeimage, ImageUploaderFallback
from common.mediainfo import MediaFile
from rich.console import Console
from common.config import config
from unit3dup.ping import offline_uploaders

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
        self.video_capture = cv2.VideoCapture(self.file_name)

    @property
    def fileName(self) -> str:
        return self.file_name

    @property
    def standard(self) -> int:
        """Determine if the video is standard definition (SD) or HD."""
        is_hd = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT) >= 720
        console.log(f"[HD]........... {'YES' if is_hd else 'NO'}")
        return 0 if is_hd else 1

    @property
    def mediainfo(self) -> str:
        """Return media info as a string."""
        # return MediaInfo.parse(self.file_name, output="STRING", full=False)
        media_info = MediaFile(self.file_name)
        return media_info.info

    @property
    def total_frames(self) -> cv2:
        """Return the total number of frames in the video."""
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def samples(self) -> cv2:
        """
        Return a list of frame numbers sampled randomly starting from 25% of the video.
        """
        start_frame = int(0.35 * self.total_frames)
        end_frame = int(0.65 * self.total_frames)
        # Create a list of random frames starting at 'start_frame'
        return random.sample(range(start_frame, end_frame), self.samples_n)

    @property
    def frames(self) -> list:
        """
        Return a list of frames as byte arrays.
        """
        frames_list = []
        for frame_number in self.samples:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()
            if not ret:
                continue

            ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            if ret:
                image_bytes = buffer.tobytes()
                frames_list.append(image_bytes)

        self.video_capture.release()
        cv2.destroyAllWindows()
        return frames_list

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
