# -*- coding: utf-8 -*-

import random
import subprocess
import io
from rich.console import Console
from PIL import Image

console = Console(log_path=False)


class VideoFrame:
    def __init__(self, video_path, num_screenshots=1):
        # File Path
        self.video_path = video_path

        # Number of screenshots from the config
        self.num_screenshots = num_screenshots

    def create(self):
        # Extract screenshots
        frames = self._extract()

        # Will be encoded to base64 before uploading
        frames_in_bytes = []
        is_hd = 0
        for idx, frame in enumerate(frames):
            # Convert to bytes
            img_bytes = self.image_to_bytes(frame)

            # Check if image is HD
            is_hd = 0 if frame.height >= 720 else 1

            # Add a new frame to list
            frames_in_bytes.append(img_bytes)
        return frames_in_bytes, is_hd

    def image_to_bytes(self, frame):

        # Resize image for the tracker
        resized_image = self.resize_image(frame)

        # Convert and save to memory
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")

        # Return in bytes
        return buffered.getvalue()

    def resize_image(self, image, width=350):
        # Get aspect ratio
        aspect_ratio = image.width / image.height
        height = int(width / aspect_ratio)

        # Resize the image
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        return resized_image

    def _extract(self):
        duration = self._get_video_duration()

        # Time limit (%)
        min_time = duration * 0.35
        max_time = duration * 0.65

        # Random (uniform) numbers
        times = [random.uniform(min_time, max_time) for _ in range(self.num_screenshots)]

        # Extract frames
        frames = [self._extract_frame(time) for time in times]
        return frames

    def _get_video_duration(self):
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            self.video_path
        ]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
        except FileNotFoundError:
            console.log("[FFMPEG-ffprobe not found] - Install ffmpeg or check your system path", style="red bold")
            exit(1)

        if process.returncode != 0:
            raise RuntimeError(f'ffprobe error: {err.decode()}')

        duration = float(out.decode().strip())
        return duration

    def _extract_frame(self, time):
        # FFmpeg
        command = [
            'ffmpeg',
            '-ss', str(time),  # Speed up
            '-i', self.video_path,
            '-vframes', '1',
            '-threads', '4',
            '-f', 'image2pipe',
            '-'
        ]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
        except FileNotFoundError:
            console.log("[FFMPEG not found] - Install ffmpeg or check your system path", style="red bold")
            exit(1)

        if process.returncode != 0:
            raise RuntimeError(f'[FFmpeg] Error: {err.decode()}')

        return Image.open(io.BytesIO(out))
