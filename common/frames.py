# -*- coding: utf-8 -*-
import os
import subprocess
import io

from pathlib import Path
from PIL import Image

from common import config_settings
from view import custom_console

class VideoFrame:
    def __init__(self, video_path: str, num_screenshots: int):
        """
        Initialize VideoFrame object

        :param video_path: Path to the video file
        :param num_screenshots: Number of screenshots to take
        """
        self.video_path = Path(video_path)
        # Number of screenshots based on the user's preferences
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
        :compress_level: compressione level (0-9); 9=Max; default=4 ; 0 = best
        """
        image = self.resize_image(frame)
        buffered = io.BytesIO()
        user_compress_level: int = config_settings.user_preferences.COMPRESS_SCSHOT\
            if 0 <= config_settings.user_preferences.COMPRESS_SCSHOT <= 9 else 4
        image.save(
            buffered, format="PNG", optimize=True, compress_level=user_compress_level
        )
        return buffered.getvalue()

    @staticmethod
    def resize_image(image: Image, width: int = 650) -> Image:
        """
        Resize the image while maintaining aspect ratio

        :param image: The image to resize
        :param width: The width to resize to
        :return: Resized image
        """
        if config_settings.user_preferences.RESIZE_SCSHOT:
            aspect_ratio = image.width / image.height
            height = round(width / aspect_ratio)
            resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
            return resized_image
        else:
            return image

    def _extract(self):
        """
        Extract frames from the video based on the number of screenshots

        :return: A list of frames
        """
        duration = self._get_video_duration()
        min_time = duration * 0.35
        max_time = duration * 0.85
        interval = int(max_time - min_time)
        duration_step = interval // self.num_screenshots
        min_time = int(min_time)
        max_time = int(max_time)
        frames = [self._extract_frame(time) for time in range(min_time + duration_step, max_time, duration_step)]

        if len(frames) < self.num_screenshots:
            frames.append(self._extract_frame(max_time))
        return frames

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

    def _extract_frame(self, time_: float) -> Image:
        """
        Extract a single frame from the video at the specified time

        :param time: The time to extract the frame
        :return: The extracted frame as a PIL Image
        :raises RuntimeError: If it fails
        """
        command = [
            "ffmpeg",
            "-ss",
            str(time_),
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
            custom_console.bot_error_log(f"IMAGES Error: Please verify if your file is corrupted")
            exit(1)
        except subprocess.TimeoutExpired:
            custom_console.bot_error_log(f"IMAGES Error: Time Out. Please verify if your file is corrupted")
            exit(1)
        except FileNotFoundError:
            custom_console.bot_error_log(
                "[FFMPEG not found] - Install ffmpeg or check your system path")
            exit(1)
        except Image.UnidentifiedImageError as e:
            custom_console.bot_error_log(f"IMAGES Error: {self.video_path}  Cannot identify image file. "
                                         f"Please verify if your file is corrupted")
            exit(1)

    @staticmethod
    def create_webp_from_video(video_path, start_time, video_height, duration, output_path):
        """
        Create a webp file

        :param time: The time to extract the frame
        :param duration: how many sec
        :return: The extracted frame as a PIL Image
        :raises RuntimeError: If it fails
        : remove hostimage from the unit3d whitelist or resize it:
        :https://wsrv.nl/ 71kk pixel limit and 10sec timeout processing for the whitelisted in Unit3d
        """
        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-t", str(duration),
            "-i", video_path,
            "-vf", f"fps=7",
            "-c:v", "libwebp",
            "-quality", "50",
            "-loop", "0", # infinite
            "-f", "webp",
            output_path
        ]

        try:
            subprocess.run(command, capture_output=True, check=True)
            if not os.path.isfile(output_path):
                print(f"file {output_path} doesn't exist !")
                exit(1)
            webp_file = open(output_path, "rb")
            webp_file_content = webp_file.read()
            webp_file.close()
            os.remove(output_path)
            custom_console.bot_log(f"webp file {output_path} created")
            return [webp_file_content]

        except subprocess.CalledProcessError as e:
            custom_console.bot_error_log(f"IMAGES Error: Please verify if your file is corrupted {e}")
        except FileNotFoundError:
            custom_console.bot_error_log(
                "[FFMPEG not found] - Install ffmpeg or check your system path")
            exit(1)
        except Image.UnidentifiedImageError as e:
            custom_console.bot_error_log(f"IMAGES Error: {output_path}  Cannot identify image file. "
                                         f"Please verify if your file is corrupted")



