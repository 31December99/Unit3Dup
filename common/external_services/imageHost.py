# -*- coding: utf-8 -*-

import base64
import json
import time
import requests

from common import config
from abc import ABC, abstractmethod
from common.custom_console import custom_console


class ImageUploader(ABC):
    def __init__(self, image: bytes, key: str):
        self.image = base64.b64encode(image)
        self.key = key

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
                    self.get_endpoint(), data = data, files = files, timeout = 10
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
                custom_console.bot_log(f"[{self.__class__.__name__}] JSONDecodeError:"
                       f" Connection issue. Please check your connection")
                exit()
            except requests.exceptions.Timeout:
                custom_console.bot_log(
                    f"[{self.__class__.__name__}] We did not receive a response from the server"
                    f" within the 10 second limit"
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

    priority= config.IMGBB_PRIORITY
    def get_endpoint(self) -> str:
        return "https://api.imgbb.com/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
        }

    def get_field_name(self) -> str:
        return 'image'

class Freeimage(ImageUploader):

    priority = config.FREE_IMAGE_PRIORITY
    def get_endpoint(self) -> str:
        return "https://freeimage.host/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
            "format": "json",
        }

    def get_field_name(self) -> str:
        return 'image'

class LensDump(ImageUploader):

    priority= config.LENSDUMP_PRIORITY
    def get_endpoint(self) -> str:
        return "https://lensdump.com/api/1/upload"

    def get_data(self) -> dict:
        return {
            "key": self.key,
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
    def result(response: dict, uploader_host: str) -> str:

        if uploader_host == "Freeimage":
            return response["image"]["image"]["url"]

        if uploader_host == "ImgBB":
            return response["data"]["image"]["url"]

        if uploader_host == "LensDump":
            return response['image']['url']

