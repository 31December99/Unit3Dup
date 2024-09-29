# -*- coding: utf-8 -*-

import random
import subprocess
import io
from pathlib import Path
from PIL import Image
from common.custom_console import custom_console
from common.config import config


class VideoFrame:
    def __init__(self, video_path: str, num_screenshots: int = 3):
        """
        Initialize VideoFrame object

        :param video_path: Path to the video file
        :param num_screenshots: Number of screenshots to take
        """
        self.video_path = Path(video_path)
        self.num_screenshots = num_screenshots

    def create(self):
        """
        Create screenshots from the video

        :return: A list of screenshots in bytes and a flag indicating if any screenshot is HD
        """
        frames = self._extract()
        frames_in_bytes = []
        is_hd = 0

        for idx, frame in enumerate(frames):
            img_bytes = self.image_to_bytes(frame=frame)
            is_hd = 0 if frame.height >= 720 else 1
            frames_in_bytes.append(img_bytes)

        return frames_in_bytes, is_hd

    def image_to_bytes(self, frame: Image) -> bytes:
        """
        Convert an image to bytes

        :param frame: The image to convert
        :return: Image in bytes
        :compress_level: compressione level (0-9); 9=Max;  default=6
        """
        resized_image = self.resize_image(frame)
        buffered = io.BytesIO()
        resized_image.save(
            buffered, format="PNG", optimize=True, compress_level=config.COMPRESS_SCSHOT
        )
        return buffered.getvalue()

    def resize_image(self, image: Image, width: int = 350) -> Image:
        """
        Resize the image while maintaining aspect ratio

        :param image: The image to resize
        :param width: The width to resize to
        :return: Resized image
        """
        aspect_ratio = image.width / image.height
        height = round(width / aspect_ratio)
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        return resized_image

    def _extract(self):
        """
        Extract frames from the video at random times

        :return: A list of frames
        """
        duration = self._get_video_duration()
        min_time = duration * 0.35
        max_time = duration * 0.65
        times = [
            random.uniform(min_time, max_time) for _ in range(self.num_screenshots)
        ]
        return [self._extract_frame(time) for time in times]

    def _get_video_duration(self) -> float:
        """
        Get the duration of the video

        :return: Duration of the video in seconds
        :raises RuntimeError: If ffprobe fails
        """
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(self.video_path),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            duration = float(result.stdout.strip())
        except subprocess.CalledProcessError:
            custom_console.bot_error_log(
                f"ffprobe error: The media is invalid {self.video_path}"
            )
            exit(1)
        except FileNotFoundError:
            custom_console.bot_error_log(
                "[FFMPEG-ffprobe not found] - Install ffmpeg or check your system path"
            )
            exit(1)
        return duration

    def _extract_frame(self, time: float) -> Image:
        """
        Extract a single frame from the video at the specified time.

        :param time: The time to extract the frame.
        :return: The extracted frame as a PIL Image.
        :raises RuntimeError: If ffmpeg fails.
        """
        command = [
            "ffmpeg",
            "-ss",
            str(time),
            "-i",
            str(self.video_path),
            "-vframes",
            "1",
            "-threads",
            "4",
            "-f",
            "image2pipe",
            "-",
        ]
        try:
            result = subprocess.run(command, capture_output=True, check=True, timeout=20)
            return Image.open(io.BytesIO(result.stdout))
        except subprocess.CalledProcessError as e:
            custom_console.bot_error_log(f"[FFmpeg] Error: Please verify if your file is corrupt")
            exit(1)
        except subprocess.TimeoutExpired:
            custom_console.bot_error_log(f"[FFmpeg] Error: Time Out. Please verify if your file is corrupt")
            exit(1)
        except FileNotFoundError:
            custom_console.bot_error_log(
                "[FFMPEG not found] - Install ffmpeg or check your system path",
                style="red bold",
            )
            exit(1)

