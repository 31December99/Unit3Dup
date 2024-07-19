# -*- coding: utf-8 -*-
import base64
import sys

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
        try:
            response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error = response.json()
            console.log(f"[Report IMGBB] Screenshot {error['error']['message']} - Renew your API KEY")
            sys.exit()
