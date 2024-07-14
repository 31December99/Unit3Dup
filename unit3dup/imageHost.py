# -*- coding: utf-8 -*-
import base64
import requests
from decouple import Config, RepositoryEnv
from rich.console import Console

config_load = Config(RepositoryEnv('service.env'))
IMGBB_KEY = config_load('IMGBB_KEY')
console = Console()


class ImgBB:

    def __init__(self, image: bytes):
        self.image = base64.b64encode(image)

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
