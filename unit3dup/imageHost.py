# -*- coding: utf-8 -*-
import base64
import json
import sys
import requests
from rich.console import Console

console = Console()


class ImgBB:

    def __init__(self, image: bytes, imgbb_key: str):
        self.image = base64.b64encode(image)
        self.IMGBB_KEY = imgbb_key

    @property
    def upload(self):
        params = {
            "key": self.IMGBB_KEY,
        }

        files = {
            "image": (None, self.image),
        }

        upload_n = 0
        while upload_n < 5:
            """
            Send the image, and if we get 502 error, wait for a while
            """
            try:
                upload_n += 1
                response = requests.post(
                    "https://api.imgbb.com/1/upload", params=params, files=files
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                try:
                    message = json.loads(e.response.content.decode('utf8'))
                    if message['status_code'] == 400:
                        print(f"[Error IMGBB] '{message['error']['message']}'")
                        break
                    else:
                        print(f"[Report IMGBB try n° {upload_n}]-> {message['error']['message']}")
                except json.decoder.JSONDecodeError:
                    print(f"HTTPError received: {e.response.content.decode('utf8')}")
            except json.decoder.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                break

        console.log("Unable to upload image, try Renew your API KEY")
        sys.exit()
