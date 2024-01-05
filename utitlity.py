#!/usr/bin/env python3.9
import re
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
    # todo: rimvuoere '.' senza rimuoverli da DD5.1 H.264 ecc
    marks = ['.', ',', ';', ':', '!', '?', '"', '(', ')', '[', ']', '{', '}', '/', '\\', '&', '*',
             '$', '%', '#', '@', '_', '+']  # '-','’' ,'\'','–'

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, ' ')
        name = name.split()
        return ' '.join(name)

    # - rimuovo lettere accentate non sempre presenti in entrambi le parti
    @staticmethod
    def accented_remove(string: str):

        accented_letters = ['à', 'è', 'é', 'ì', 'ò', 'ù', 'á', 'í', 'ó', 'ú', 'ñ', 'ä', 'ö', 'ü', 'ß', 'â',
                            'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü', 'ÿ', 'ç', 'ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ä', 'ë',
                            'ï', 'ö', 'ü', 'ÿ', 'á', 'é', 'í', 'ó', 'ú', 'å', 'ä', 'ö', 'æ', 'ø', 'ş', 'ç',
                            'ğ', 'ı', 'ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'š']

        return ''.join(char for char in string if char.lower() not in accented_letters)

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
        type_dict = {
            "full-disc": 1,
            "remux": 2,
            "encode": 3,
            "web-dl": 4,
            "webdl": 4,
            "web-dlmux": 4,
            "webrip": 5,
            "hdtv": 6,
            "flac": 7,
            "alac": 8,
            # "ac3": 9,
            # "aac": 10,
            # "mp3": 11,
            "mac": 12,
            "windows": 13,
            "cinema": 14,
            "altro": 15,
            "pdf": 16,
            "nintendo": 17,
            "ps4": 18,
            "epub": 19,
            "mp4": 20,
            "pack": 22,
            "avi": 23,
        }

        for word in word_list:
            for key, value in type_dict.items():
                if word == key:
                    print(f"\n[TYPE]................  {word.upper()}\n")
                    return type_dict[word]

        # Se non trova la keyword 'codec' cerca eventuali nomi di codec
        if Manage_titles.filterCodec(file_name):
            return type_dict['encode']  # encode
        return type_dict['altro']

    @staticmethod
    def filterCodec(file_name: str) -> bool:
        word_list = file_name.lower().strip().split(" ")
        video_codecs = [
            "h261",
            "h262",
            "h263",
            "h264",
            "x264",
            "x265",
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
            "vp3",
            "vp2",
            "vp1",
            "amv",
            "daala",
            "gecko",

        ]
        for word in word_list:
            if word in video_codecs:
                return True
        return False

    @staticmethod
    def filterResolution(file_name: str) -> int:

        file_name = Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")

        resulution_dict = {
            "4320p": 1,
            "2160p": 2,
            "1080p": 3,
            "1080i": 4,
            "720p": 5,
            "576p": 6,
            "576i": 7,
            "480p": 8,
            "480i": 9,
            "altro": 10,
        }
        for word in word_list:
            for key, value in resulution_dict.items():
                if word == key:
                    return resulution_dict[word]
        return resulution_dict['altro']
