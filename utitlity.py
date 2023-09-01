#!/usr/bin/env python3.9


class Manage_titles:
    marks = [',', ';', ':', '!', '?', '"', '(', ')', '[', ']', '{', '}', '/', '\\', '&', '*',
             '$', '%', '#', '@', '_']

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, '')
        return name

    @staticmethod
    def filterType(file_name: str) -> int:
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
