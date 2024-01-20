# -*- coding: utf-8 -*-
import random
import cv2
import os
import imageHost
from pymediainfo import MediaInfo
from decouple import config

PASS_KEY = config('PASS_KEY')
API_TOKEN = config('API_TOKEN')


class Video:
    """
     Questa classe deve poter:

     - generare screenshot per ogni video che gli viene passato
     - ottenere mediainfo per ogni video che gli viene passato e per il primo video di una serie
     - caricare su imgBB gli screenshot
     - resituire il size del video ad esempio per determinare il freelech
     - determinare se è qualità standard (SD) o meno

    """

    def __init__(self, fileName: str):

        self.file_name = fileName
        # video file size
        self.file_size = round(os.path.getsize(self.file_name) / (1024 * 1024 * 1024))
        # Frame count
        self.numero_di_frame = None
        # Screenshots samples
        self.samples_n = 6
        # Catturo i frames del video
        print(f"[ CAPTURING SCREEN... ]")
        self.video_capture = cv2.VideoCapture(self.file_name)

    @property
    def fileName(self) -> str:
        return self.file_name

    @property
    def standard(self) -> int:
        # SD o HD ?
        if self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) < 720:
            print(f"[HD]........... YES")
            return 1
        else:
            print(f"[HD]........... NO")
            return 0

    @property
    def size(self) -> int:
        """
        :return: size in Gb
        """
        return self.file_size

    @property
    def mediainfo(self) -> str:
        """
        :return: media info in string format
        """
        return MediaInfo.parse(self.file_name, output="STRING", full=False)

    @property
    def totalFrames(self) -> cv2:
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
        inizia_da = int(.25 * self.totalFrames)
        # Genero una lista di frame casuali che partono dal 25% del video
        return random.sample(range(inizia_da, self.totalFrames), self.samples_n)

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
            screenshot_name = f'screenshot_{frame_number}.jpg'
            frames_list.append(screenshot_name)
            quality = 90
            cv2.imwrite(screenshot_name, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

        self.video_capture.release()
        cv2.destroyAllWindows()
        return frames_list

    @property
    def description(self) -> str:
        descrizione = f"[center]\n"
        for f in self.frames:
            img_host = imageHost.ImgBB(f)
            img_url = img_host.upload['data']['display_url']
            descrizione += (f"[url={img_url}][img=350]"
                            f"{img_url}[/img][/url]")
        descrizione += "\n[/center]"
        return descrizione
