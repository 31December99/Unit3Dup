# -*- coding: utf-8 -*-
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
        print(f"[IMG]..........  {response.json()['data']['url_viewer']}")
        return response.json()
