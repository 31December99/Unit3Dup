#!/usr/bin/env python3.9
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Console:

    @staticmethod
    def print(message: str, level: int):
        now = datetime.now()
        date_now = datetime.today().strftime('%d-%m-%Y')
        time_now = now.strftime("%H:%M:%S")
        if level == 1:
            print(f"<{date_now} {time_now}>{bcolors.FAIL}{message}{bcolors.ENDC}")
        if level == 2:
            print(f"<{date_now} {time_now}>{bcolors.OKGREEN}{message}{bcolors.ENDC}")
        if level == 3:
            print(f"<{date_now} {time_now}>{bcolors.WARNING}{message}{bcolors.ENDC}")


class Manage_titles:
    marks = ['.', ',', ';', ':', '!', '?', '"', '(', ')', '[', ']', '{', '}', '/', '\\', '&', '*',
             '$', '%', '#', '@', '_', '-']

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, ' ')
        name = name.split()
        return ' '.join(name)


    @staticmethod
    def filterType(file_name: str) -> int:
        """
        Cerca le keyword nel titolo
        Cerca eventuali codec nel titolo e lo setta come codice con il valore di ritorno
        :param file_name:
        :return:
        """
        file_name = Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")
        lista = [
            "fulldisc",
            "remux",
            "encode",
            "web-dl",
            "webrip",
            "hdtv",
            "flac",
            "alac",
            "ac3",
            "mp3",
            "mac",
            "windows",
            "cinema",
            "altro",
            "pdf",
            "nintendo",
            "ps4",
            "epub",
            "mp4",
            "pack",
            "avi",
        ]

        for word in word_list:
            if word in lista:
                return lista.index(word) + 1

        if Manage_titles.filterCodec(file_name):
            return 2  # encode

        return 15  # Altro

    @staticmethod
    def filterCodec(file_name: str) -> bool:

        file_name = Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")

        video_codecs = [
            "h261",
            "h262",
            "h263",
            "h264",
            "avc",
            "h265",
            "hevc",
            "vp8",
            "vp9",
            "av1",
            "mpeg-1",
            "mpeg-4",
            "wmv",
            "theora",
            "divx",
            "xvid",
            "prores",
            "dnxhd",
            "cinepak",
            "indeo",
            "dv",
            "ffv1",
            "sorenson",
            "rv40",
            "cineform",
            "huffyuv",
            "mjpeg",
            "lagarith",
            "msu",
            "rle",
            "dirac",
            "wmv3",
            "vorbis",
            "smpte",
            "mjpeg",
            "ffvhuff",
            "v210",
            "yuv4:2:2",
            "yuv4:4:4",
            "hap",
            "sheervideo",
            "ut",
            "quicktime",
            "rududu",
            "h.266",
            "vvc",
            "mjpeg 4:2:0",
            "h.263+",
            "h.263++",
            "vp4",
            "vp5",
            "vp6",
            "vp7",
            "vp8",
            "vp9",
            "vp10",
            "vp11",
            "vp12",
            "theora (tremor)",
            "theora (libtheora)",
            "vp3",
            "vp2",
            "vp1",
            "amv",
            "daala",
            "gecko"
        ]
        for word in word_list:
            if word in video_codecs:
                return True
        return False
