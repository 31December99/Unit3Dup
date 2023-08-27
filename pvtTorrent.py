#!/usr/bin/env python3.9
import random
import base64
import cv2
import torf
import requests
import os
from decouple import config

IMGBB_KEY = config('IMGBB_KEY')


class Screenshot:

    def __init__(self, file_name):
        self.numero_di_frame = None
        self.file_name = file_name
        self.samples_n = 7
        self.video_capture = cv2.VideoCapture(self.file_name)
        self.standard = 1 if self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) < 720 else '0'


    @property
    def total_frames(self) -> cv2:
        """

        :return: il numero di frames che compongono il video
        """
        # Calcolo il numero di frame del video
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def samples(self) -> cv2:
        """

        :return: un lista di sample_n frame con posizione casuale che partono 25% del video
        """
        inizia_da = int(.25 * self.total_frames)
        # Genero una lista di frame casuali che partono dal 25% del video
        return random.sample(range(inizia_da, self.total_frames), self.samples_n)

    @property
    def frames(self) -> list:
        """

        :return: una lista di filename frames in formato jpg
        """

        frames_list = []
        for frame_number in self.samples:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()
            if not ret:
                continue
            screenshot_name = f'screenshot_{frame_number}.png'
            print(screenshot_name)
            frames_list.append(screenshot_name)
            cv2.imwrite(screenshot_name, frame)
        self.video_capture.release()
        cv2.destroyAllWindows()
        return frames_list


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


class Mytorrent:

    def __init__(self, file_name):
        self.file_name = file_name
        self.mytorr = torf.Torrent(path=self.file_name)
        self.mytorr.generate()
        self.mytorr.created_by = "bITT"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB

    def get_screenshots(self):
        return Screenshot(self.file_name)

    def write(self, torrent_filename: str):
        self.mytorr.write(f"{torrent_filename}.torrent")

    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def name(self):
        return self.mytorr.name

    @name.setter
    def name(self, value):
        self.mytorr.name = value

    @property
    def info_hash(self):
        return self.mytorr.infohash
