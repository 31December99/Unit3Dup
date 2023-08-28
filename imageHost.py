#!/usr/bin/env python3.9
import base64
import os
import requests
from decouple import config

IMGBB_KEY = config('IMGBB_KEY')


class ImgHost:

    def __init__(self, filename: str):
        self.filename = filename
        self.params = {}
        self.file = {}

    @property
    def image(self) -> base64:
        if os.path.exists(self.filename):
            open_image = open(self.filename, 'rb')
            image_data = open_image.read()
            return base64.b64encode(image_data)

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
