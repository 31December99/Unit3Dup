#!/usr/bin/env python3.9
import random
import cv2
import os
import pvtTorrent
import imageHost
from pymediainfo import MediaInfo
from decouple import config

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')


class Video:
    """
     Questa classe deve poter:

     - generare screenshot per ogni video che gli viene passato
     - ottenere mediainfo per ogni video che gli viene passato e per il primo video di una serie
     - caricare su imgBB gli screenshot
     - resituire il size del video ad esempio per determinare il freelech
     - determinare se è qualità standard (SD) o meno

    """

    def __init__(self, contents: str):
        self.contents = contents
        if os.path.isdir(self.contents):
            self.folder_name = os.path.basename(self.contents)
            self.file_name = os.listdir(self.contents)[0]
            self.mytorrent = pvtTorrent.Mytorrent(contents=self.contents)

        else:
            self.file_name = self.contents
            self.mytorrent = pvtTorrent.Mytorrent(contents=self.file_name)

        # video file size
        self.file_size = None
        # Frame count
        self.numero_di_frame = None
        # Screenshots samples
        self.samples_n = 6
        # Catturo i frames del video
        self.video_capture = cv2.VideoCapture(self.file_name)

    @property
    def torrentName(self) -> str:
        return self.mytorrent.name

    @property
    def freeLech(self) -> int:
        return self._freelech()

    @property
    def fileName(self) -> str:
        return self.file_name

    @property
    def folderName(self) -> str:
        return self.folder_name

    @property
    def standard(self) -> int:
        # is this a standard video ?
        return 1 if self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) < 720 else '0'

    @property
    def size(self) -> int:
        """
        :return: size in Gb
        """
        self.file_size = os.path.getsize(self.file_name)
        return round(self.file_size / (1024 * 1024 * 1024))

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
            print(screenshot_name)
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
            descrizione += (f"[url={img_host.upload['data']['display_url']}][img=350]"
                            f"{img_host.upload['data']['display_url']}[/img][/url]")
        descrizione += "\n[/center]"

        return descrizione

    @property
    def torrent(self) -> pvtTorrent:
        self.mytorrent.write()
        return self.mytorrent

    def _freelech(self) -> int:
        if self.size >= 20:
            return 100
        elif self.size >= 15:
            return 75
        elif self.size >= 10:
            return 50
        elif self.size >= 5:
            return 25
        else:
            return 0
