# -*- coding: utf-8 -*-
import base64
import os
import requests
from decouple import Config, RepositoryEnv
from rich.console import Console

config_load = Config(RepositoryEnv('service.env'))
IMGBB_KEY = config_load('IMGBB_KEY')
console = Console()


class ImgHost:

    def __init__(self, filename: str):
        self.filename = os.path.join("images", filename)
        self.params = {}
        self.file = {}

    @property
    def image(self) -> base64:
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as open_image:
                image_data = open_image.read()
                image_encode = base64.b64encode(image_data)
            os.remove(self.filename)
            return image_encode

    def upload(self):
        pass


class ImgBB(ImgHost):

    @property
    def upload(self):
        params = {
            'key': IMGBB_KEY,
        }

        files = {
            'image': (None, self.image),
        }
        response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
        return response.json()
