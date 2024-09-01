# -*- coding: utf-8 -*-

import base64
import json
import time
import requests

from abc import ABC, abstractmethod
from common.custom_console import custom_console


class ImageUploader(ABC):
    def __init__(self, image: bytes, key: str):
        self.image = base64.b64encode(image)
        self.key = key

    @abstractmethod
    def get_endpoint(self):
        return "https://api.imgbb.com/1/upload"

    @abstractmethod
    def get_params(self):
        return {
            "key": self.key,
        }

    def upload(self):
        params = self.get_params()
        files = {
            "image": (None, self.image),
        }

        upload_n = 0
        while upload_n < 4:
            try:
                upload_n += 1
                response = requests.post(
                    self.get_endpoint(), params=params, files=files, timeout=10
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                self.handle_http_error(e, upload_n)
                time.sleep(1)

            except json.decoder.JSONDecodeError as e:
                custom_console.bot_log(f"[Imagehost] JSONDecodeError: {e}")
                break

            except requests.exceptions.Timeout:
                custom_console.bot_log(
                    "'[Timeout]' We did not receive a response from the server within the 10 second limit"
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


class Freeimage(ImageUploader):

    def get_endpoint(self) -> str:
        return "https://freeimage.host/api/1/upload"

    def get_params(self) -> dict:
        return {
            "key": self.key,
            "format": "json",
        }


class ImgBB(ImageUploader):

    def get_endpoint(self) -> str:
        return "https://api.imgbb.com/1/upload"

    def get_params(self) -> dict:
        return {
            "key": self.key,
        }


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
            custom_console.bot_log(
                f"[{self.uploader.__class__.__name__}]..... [ON-LINE]"
            )
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
            return response["image"]["display_url"]

        if uploader_host == "ImgBB":
            return response["data"]["display_url"]
