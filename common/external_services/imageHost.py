# -*- coding: utf-8 -*-

import base64
import json
import time
import requests

from abc import ABC, abstractmethod
from common import config_settings
from view import custom_console


class ImageUploader(ABC):
    def __init__(self, image: bytes, key: str, image_name: str):
        self.image = base64.b64encode(image)
        self.key = key
        self.image_name = image_name

    @abstractmethod
    def get_endpoint(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_field_name(self):
        pass

    def upload(self):
        data = self.get_data()
        files = {
            self.get_field_name(): (None, self.image),
        }

        upload_n = 0
        while upload_n < 4:
            try:
                upload_n += 1
                response = requests.post(
                    self.get_endpoint(), data = data, files = files, timeout = 30
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                self.handle_http_error(e, upload_n)
                time.sleep(1)

            except requests.exceptions.ConnectionError as e:
                custom_console.bot_log(f"[{self.__class__.__name__}] JSONDecodeError: {e}")
                break

            except json.decoder.JSONDecodeError as e:
                # or Maintenance mode
                custom_console.bot_log(f"[{self.__class__.__name__}] JSONDecodeError"
                       f" Connection issue. Please check your connection or the website")
                break
            except requests.exceptions.Timeout:
                custom_console.bot_log(
                    f"[{self.__class__.__name__}] We did not receive a response from the server"
                    f" within the 20 second limit"
                )
                break

        return None

    def handle_http_error(self, error, attempt):
        try:
            message = json.loads(error.response.content.decode("utf8"))
            if message.get("status_code") == 400:
                custom_console.bot_error_log(
                    f"[Error {self.__class__.__name__}] '{message['error']['message']}'"
                )
            else:
                custom_console.bot_error_log(
                    f"[Report {self.__class__.__name__} try n° {attempt}]-> {message['error']['message']}"
                )

        except json.decoder.JSONDecodeError:
            custom_console.bot_error_log(f"HTTPError received: {error}")


class ImgBB(ImageUploader):

    priority= config_settings.user_preferences.IMGBB_PRIORITY
    def get_endpoint(self) -> str:
        return "https://api.imgbb.com/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "name": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'image'


class Freeimage(ImageUploader):

    priority = config_settings.user_preferences.FREE_IMAGE_PRIORITY
    def get_endpoint(self) -> str:
        return "https://freeimage.host/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "format": "json",
            "name": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'image'


class PtScreens(ImageUploader):

    priority= config_settings.user_preferences.PTSCREENS_PRIORITY
    def get_endpoint(self) -> str:
        return "https://ptscreens.com/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "title": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'source'


class LensDump(ImageUploader):

    priority= config_settings.user_preferences.LENSDUMP_PRIORITY
    def get_endpoint(self) -> str:
        return "https://lensdump.com/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "title": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'source'


class ImgFi(ImageUploader):

    priority= config_settings.user_preferences.IMGFI_PRIORITY
    def get_endpoint(self) -> str:
        return "https://imgfi.com/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "title": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'source'

class PassIMA(ImageUploader):

    priority= config_settings.user_preferences.PASSIMA_PRIORITY
    def get_endpoint(self) -> str:
        return "https://passtheima.ge/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "title": self.image_name,
        }

    def get_field_name(self) -> str:
        return 'source'


class ImageUploaderFallback:
    def __init__(self, uploader):
        self.uploader = uploader

    def upload(self, test=False) -> str:
        result = None

        # Get response from the uploader
        response = self.uploader.upload()

        # If not None get a new url
        if response:
            result = ImageUploaderFallback.result(
                response=response, uploader_host=self.uploader.__class__.__name__
            )

        # If there is no error from json response
        if result:
            """
            custom_console.bot_log(f"[{self.uploader.__class__.__name__}]..... [ON-LINE]")
            """
            if not test:
                return result

        # send an off-line message
        if not result:
            custom_console.bot_log(
                f"[{self.uploader.__class__.__name__}]..... [OFF-LINE]"
            )
        return result

    @staticmethod
    def result(response: dict, uploader_host: str) -> str | None:

        if uploader_host == "Freeimage":
            return response["image"]["image"]["url"]

        if uploader_host == "ImgBB":
            return response["data"]["image"]["url"]

        if uploader_host == "LensDump":
            return response['image']['url']

        if uploader_host == "PtScreens":
            return response['image']['url']

        if uploader_host == "ImgFi":
            return response['image']['url']

        if uploader_host == "PassIMA":
            return response['image']['url']

        return None

class Build:
    """
    - Upload screenshots and create a new description
    """
    offline_uploaders = []

    def __init__(self, extracted_frames: list[bytes], filename: str):

        # Image filename
        self.filename = filename

        # Host APi keys
        self.IMGBB_KEY = config_settings.tracker_config.IMGBB_KEY
        self.FREE_IMAGE_KEY = config_settings.tracker_config.FREE_IMAGE_KEY
        self.LENSDUMP_KEY= config_settings.tracker_config.LENSDUMP_KEY
        self.PTSCREENS_KEY= config_settings.tracker_config.PTSCREENS_KEY
        self.IMGFI_KEY = config_settings.tracker_config.IMGFI_KEY
        self.PASSIMA_KEY = config_settings.tracker_config.PASSIMA_KEY
        self.extracted_frames = extracted_frames


    def description(self) -> str:
        description = "[center]\n"
        console_url = []

        custom_console.bot_log("Starting image upload..")
        _number = 0
        for img_bytes in self.extracted_frames:
            _number = _number + 1
            image_name = f"{self.filename}.id_{_number}"

            master_uploaders = [
                ImgBB(img_bytes, self.IMGBB_KEY, image_name=image_name),
                Freeimage(img_bytes, self.FREE_IMAGE_KEY,image_name=image_name),
                PtScreens(img_bytes, self.PTSCREENS_KEY,image_name=image_name),
                LensDump(img_bytes, self.LENSDUMP_KEY,image_name=image_name),
                ImgFi(img_bytes, self.IMGFI_KEY,image_name=image_name),
                PassIMA(img_bytes, self.PASSIMA_KEY, image_name=image_name),
            ]

            # Sorting list based on priority
            master_uploaders.sort(key=lambda uploader: uploader.priority)

            # for each on-line uploader
            for uploader in master_uploaders:
                if not uploader.__class__.__name__ in self.offline_uploaders:
                    # Upload the screenshot
                    fallback_uploader = ImageUploaderFallback(uploader)
                    # Get a new URL
                    img_url = fallback_uploader.upload()

                    # If it goes offline during upload skip the uploader
                    if not img_url:
                        custom_console.bot_error_log(
                            "** Upload failed, skip to next host **"
                        )
                        self.offline_uploaders.append(uploader.__class__.__name__)
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

