# -*- coding: utf-8 -*-
import os
import datetime
import re
from datetime import datetime
from thefuzz import fuzz


class Manage_titles:
    # todo: rimvuoere '.' senza rimuoverli da DD5.1 H.264 ecc
    marks = [
        ".",
        ",",
        ";",
        ":",
        "!",
        "?",
        '"',
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "/",
        "\\",
        "&",
        "*",
        "$",
        "%",
        "#",
        "@",
        "_",
        "+",
    ]  # '-','’' ,'\'','–'

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, " ")
        name = name.split()
        return " ".join(name)

    # - rimuovo lettere accentate non sempre presenti in entrambi le parti
    @staticmethod
    def accented_remove(string: str):
        accented_letters = [
            "à",
            "è",
            "é",
            "ì",
            "ò",
            "ù",
            "á",
            "í",
            "ó",
            "ú",
            "ñ",
            "ä",
            "ö",
            "ü",
            "ß",
            "â",
            "ê",
            "î",
            "ô",
            "û",
            "ë",
            "ï",
            "ü",
            "ÿ",
            "ç",
            "ã",
            "ẽ",
            "ĩ",
            "õ",
            "ũ",
            "ä",
            "ë",
            "ï",
            "ö",
            "ü",
            "ÿ",
            "á",
            "é",
            "í",
            "ó",
            "ú",
            "å",
            "ä",
            "ö",
            "æ",
            "ø",
            "ş",
            "ç",
            "ğ",
            "ı",
            "ą",
            "ć",
            "ę",
            "ł",
            "ń",
            "ó",
            "ś",
            "ź",
            "ż",
            "š",
        ]

        return "".join(char for char in string if char.lower() not in accented_letters)

    @staticmethod
    def filter_ext(file: str) -> bool:
        video_ext = [
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
            ".3gp",
            ".ogg",
            ".mpg",
            ".mpeg",
            ".m4v",
            ".rm",
            ".rmvb",
            ".vob",
            ".ts",
            ".m2ts",
            ".divx",
            ".asf",
            ".swf",
            ".ogv",
            ".drc",
            ".m3u8",
            ".pdf",
        ]

        return os.path.splitext(file)[1].lower() in video_ext

    @staticmethod
    def replace(subdir: str):
        res = ["4320", "2160", "1080", "720", "576", "480"]
        # wrong guessit when substring is 'S01-'
        # '-'
        subdir = subdir.replace("-", ".")
        # wrong guessit season when there are no 'p' or 'i' in then subdir string
        for wrong_res in res:
            subdir = subdir.replace(wrong_res, ' ')
        return subdir

    @staticmethod
    def media_docu_type(file_name: str) -> str:
        ext = os.path.splitext(file_name)[1].lower()
        type_ = {".pdf": "edicola"}

        return type_.get(ext, None)

    @staticmethod
    def fuzzyit(str1: str, str2: str) -> int:
        return fuzz.ratio(str1.lower(), str2.lower())


class MyString:

    @staticmethod
    def parse_date(line_str: str) -> datetime | None:
        """
        Parse a string with or without time
        """

        # Case string with time attribute
        match_time = re.search(r"(\w{3})\s+(\d{1,2})\s+(\d{2}:\d{2})", line_str)

        # Case string without time attribute
        match_no_time = re.search(r"(\w{3})\s+(\d{1,2})\s+(\d{4})", line_str)

        if match_time:
            # Build a datetime object
            month, day, time = match_time.groups()
            year = datetime.now().year
            data_ora = datetime.strptime(
                f"{month} {day} {time} {year}", "%b %d %H:%M %Y"
            )

        elif match_no_time:
            # Build a datetime object with no time
            month, day, year = match_no_time.groups()
            data_ora = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
        else:
            # Invalid string
            return
        return data_ora


class System:

    @staticmethod
    def get_size(folder_path) -> float:

        # Size of single file
        if os.path.isfile(folder_path):
            return round(os.path.getsize(folder_path) / (1024**3), 2)
        else:
            # size of folder
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    if not os.path.islink(file_path):
                        total_size += os.path.getsize(file_path)
            return round(total_size / (1024**3), 2)
