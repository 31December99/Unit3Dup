# -*- coding: utf-8 -*-
import os

import diskcache
import subprocess
import unicodedata

from common.external_services.imageHost import Build
from view import custom_console
from unit3dup import config_settings
from PIL import Image

class PdfImages:
    """
    - Generate screenshots for each Document provided
    """

    def __init__(self, file_name: str):

        # File name
        self.file_name: str = file_name

        # Screenshots samples
        samples_n: int = config_settings.user_preferences.NUMBER_OF_SCREENSHOTS\
            if 2 <= config_settings.user_preferences.NUMBER_OF_SCREENSHOTS <= 10 else 4

        # Description
        self.description: str = ''

        # description cache
        self.docu_cache = diskcache.Cache(str(os.path.join(config_settings.user_preferences.CACHE_PATH, "covers.cache")))

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        # normalize !
        normalized_filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
        # replace special chars with those in list
        sanitized_filename = "".join(c if c.isalnum() or c in ['.', '-', '_'] else "_" for c in normalized_filename)
        return sanitized_filename


    def extract(self) -> list['Image']:
        images = []

        # Sanitize the input file name
        sanitized_file_name = self.sanitize_filename(os.path.basename(self.file_name))
        path = os.path.dirname(self.file_name)
        output_name = os.path.join(path, sanitized_file_name)

        command = [
            "pdftocairo",
            "-q",  # Silent
            "-singlefile", # do not add digit
            "-png",
            "-f", "1",
            "-l", "1",
            self.file_name,
            output_name,
        ]
        try:
            subprocess.run(command, capture_output=True, check=True, timeout=20)
        except subprocess.CalledProcessError:
            custom_console.bot_error_log(f"It was not possible to extract any page from '{self.file_name}'")
            exit(1)
        except FileNotFoundError:
            custom_console.bot_error_log(f"It was not possible to find 'xpdf'. Please check your system PATH or install it.")
            exit(1)

        output_name+='.png'
        with open(output_name, "rb") as img_file:
            img_data = img_file.read()
            images.append(img_data)
        if os.path.exists(output_name):
            os.remove(output_name)

        return images

    def build_info(self):
        """Build the information to send to the tracker"""

        # If cache is enabled and the title is already cached
        if config_settings.user_preferences.CACHE_SCR:
            description = self.load_cache(self.file_name)
            if isinstance(description, dict):
                self.description = description['description']
                if not self.description:
                    custom_console.bot_warning_log(f""
                                                   f"[{self.__class__.__name__}] The description in the cache is empty")
        else:
            self.description = None

        if not self.description:
            # If there is no cache available
            custom_console.bot_log(f"GENERATING PAGES..")
            extracted_frames = self.extract()
            custom_console.bot_log("Done.")
            # Create a new description
            build_description = Build(extracted_frames=extracted_frames, filename = self.file_name)
            self.description = build_description.description()

        # Write the new description to the cache
        if config_settings.user_preferences.CACHE_SCR:
            self.docu_cache[self.file_name] = {'description' : self.description}


    def load_cache(self, file_name: str):
        # Check if the item is in the cache
        if file_name not in self.docu_cache:
            return False

        custom_console.bot_warning_log(f"** {self.__class__.__name__} **: Using cached Description!")

        try:
            # Try to get the video from the cache
            cover = self.docu_cache[file_name]
        except KeyError:
            # Handle the case where the video is missing or the cache is corrupted
            custom_console.bot_error_log("Cached frame not found or cache file corrupted")
            custom_console.bot_error_log("Proceed to extract the screenshot again. Please wait..")
            return False

        # // OK
        return cover
