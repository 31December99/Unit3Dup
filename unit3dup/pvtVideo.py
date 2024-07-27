# -*- coding: utf-8 -*-
import random
import cv2
import os
from unit3dup.imageHost import ImgBB
from pymediainfo import MediaInfo
from rich.console import Console

console = Console()


class Video:
    """
        - Generate screenshots for each video provided
        - Obtain media info for each video and for the first video in a series
        - Upload screenshots to ImgBB
        - Return the video size
        - Determine if the video is standard definition (SD) or not
    """

    def __init__(self, fileName: str):

        self.file_name = fileName
        # video file size
        # TODO: in realtà occorre calcolare anche tutta la folder in caso di series.Per il momento utilizzo size di
        # TODO: Files class
        self.file_size = round(os.path.getsize(self.file_name) / (1024 * 1024 * 1024))
        # Frame count
        self.numero_di_frame = None
        # Screenshots samples
        self.samples_n = 4
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

    @property  # non utilizzare vedi nota sopra
    def size(self) -> int:
        """Return the size of the video in GB."""
        return self.file_size

    @property
    def mediainfo(self) -> str:
        """Return media info as a string."""
        return MediaInfo.parse(self.file_name, output="STRING", full=False)

    @property
    def total_frames(self) -> cv2:
        """Return the total number of frames in the video."""
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def samples(self) -> cv2:
        """
        Return a list of frame numbers sampled randomly starting from 25% of the video.
        """
        inizia_da = int(.25 * self.total_frames)
        # Genero una lista di frame casuali che partono dal 25% del video
        return random.sample(range(inizia_da, self.total_frames), self.samples_n)

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

            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            if ret:
                image_bytes = buffer.tobytes()
                frames_list.append(image_bytes)

        self.video_capture.release()
        cv2.destroyAllWindows()
        return frames_list

    @property
    def description(self) -> str:
        """Generate a description with image URLs uploaded to ImgBB."""
        console.log("\n[GENERATING IMAGES FROM VIDEO...]")
        description = "[center]\n"
        console_url = []
        for img_bytes in self.frames:
            img_host = ImgBB(img_bytes)
            img_url = img_host.upload['data']['display_url']
            console.log(img_url)
            console_url.append(img_url)
            description += (f"[url={img_url}][img=350]{img_url}[/img][/url]")
        description += "\n[/center]"
        return description
