import random
import subprocess
import io
from PIL import Image


class Screenshots:
    def __init__(self, video_path, num_screenshots=1):
        # File Path
        self.video_path = video_path

        # nume of screenshot from the config
        self.num_screenshots = num_screenshots

        # is HD ?
        self.is_hd = False

    def create(self):
        # Exstract screenshot
        frames = self._extract()

        #  will be encoded to base64 before to uploading
        frames_in_bytes = []
        for idx, frame in enumerate(frames):
            img_bytes = self.image_to_bytes(frame)
            frames_in_bytes.append(img_bytes)
        return frames_in_bytes

    def image_to_bytes(self, image):

        # is HD ?
        self.is_hd = image.height >= 720

        # Resize image for the tracker
        resized_image = self.resize_image(image)

        # Convert and save to mem
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")

        # Returns in bytes
        return buffered.getvalue()

    def resize_image(self, image, width=350):
        # Get Ratio
        aspect_ratio = image.width / image.height
        height = int(width / aspect_ratio)

        # Resize the image
        resized_image = image.resize((width, height), Image.ANTIALIAS)
        return resized_image

    def _extract(self):
        duration = self._get_video_duration()

        # Time limit (%)
        min_time = duration * 0.35
        max_time = duration * 0.65

        # Random (uniform) numbers
        times = [random.uniform(min_time, max_time) for _ in range(self.num_screenshots)]

        # Extract...
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
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f'ffprobe errore: {err.decode()}')

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

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f'[FFmpeg] Error: {err.decode()}')

        return Image.open(io.BytesIO(out))
