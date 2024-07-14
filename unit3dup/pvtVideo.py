# -*- coding: utf-8 -*-
import random
import cv2
import os
from unit3dup.imageHost import ImgBB
from pymediainfo import MediaInfo
from rich.console import Console

console = Console()

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
        self.video_capture = cv2.VideoCapture(self.file_name)

    @property
    def fileName(self) -> str:
        return self.file_name

    @property
    def standard(self) -> int:
        # SD o HD ?
        if self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) < 720:
            console.log(f"[HD]........... YES")
            return 1
        else:
            console.log(f"[HD]........... NO")
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
        :return: una lista di tuple contenenti le immagini del frame in bytes
        """
        frames_list = []
        for frame_number in self.samples:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()
            if not ret:
                continue

            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            if ret:
                image_bytes = buffer.tobytes()
                frames_list.append(image_bytes)

        self.video_capture.release()
        cv2.destroyAllWindows()
        return frames_list


    @property
    def description(self) -> str:
        console.log("\n[GENERATING IMAGES FROM VIDEO...]")
        descrizione = f"[center]\n"
        console_url = []
        for f in self.frames:
            img_host = ImgBB(f)
            img_url = img_host.upload['data']['display_url']
            console.log(img_url)
            console_url.append(img_url)
            descrizione += (f"[url={img_url}][img=350]"
                            f"{img_url}[/img][/url]")
        descrizione += "\n[/center]"
        return descrizione

