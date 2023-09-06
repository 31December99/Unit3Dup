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
        return name

    @staticmethod
    def filterType(file_name: str) -> int:
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
                # Tracker type starts from zero
                return lista.index(word) + 1
        return 15  # Altro
