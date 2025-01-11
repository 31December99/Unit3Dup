# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
from thefuzz import fuzz


class ManageTitles:
    """
    Manages file title operations like removing punctuation,
    removing accented letters, and handling file types
    """

    marks = [
        ".", ",", ";", ":", "!", "?", '"', "(", ")", "[", "]", "{", "}", "/",
        "\\", "&", "*", "$", "%", "#", "@", "_", "+"
    ]

    @staticmethod
    def clean(filename: str) -> str:
        """
        Removes special characters and replaces them with spaces
        Returns a cleaned string without punctuation
        """
        for punct in ManageTitles.marks:
            filename = filename.replace(punct, " ")
        return " ".join(filename.split())

    @staticmethod
    def accented_remove(string: str) -> str:
        """
        Removes accented characters from a string
        """
        accented_letters = [
            "à", "è", "é", "ì", "ò", "ù", "á", "í", "ó", "ú", "ñ", "ä", "ö", "ü", "ß", 
            "â", "ê", "î", "ô", "û", "ë", "ï", "ÿ", "ç", "ã", "ẽ", "ĩ", "õ", "ũ", "å", 
            "æ", "ø", "ş", "ç", "ğ", "ı", "ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż", 
            "š"
        ]
        return "".join(char for char in string if char.lower() not in accented_letters)

    @staticmethod
    def filter_ext(file: str) -> bool:
        """
        Filters files by their extensions
        Returns True if the file is a video
        """
        video_ext = [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".ogg", 
            ".mpg", ".mpeg", ".m4v", ".rm", ".rmvb", ".vob", ".ts", ".m2ts", ".divx", 
            ".asf", ".swf", ".ogv", ".drc", ".m3u8", ".pdf"
        ]
        return os.path.splitext(file)[1].lower() in video_ext

    @staticmethod
    def replace(subdir: str) -> str:
        """
        Replaces hyphens with dots and removes video resolutions
        """
        resolutions = ["4320", "2160", "1080", "720", "576", "480"]
        subdir = subdir.replace("-", ".")
        for res in resolutions:
            subdir = subdir.replace(res, " ")
        return subdir

    @staticmethod
    def media_docu_type(file_name: str) -> str:
        """
        Returns document type based on file extension
        """
        ext = os.path.splitext(file_name)[1].lower()
        type_ = {".pdf": "edicola"}
        return type_.get(ext, None)

    @staticmethod
    def fuzzyit(str1: str, str2: str) -> int:
        """
        Returns similarity score between two strings
        """
        return fuzz.ratio(str1.lower(), str2.lower())


class MyString:
    """
    Handles string operations like date parsing
    """

    @staticmethod
    def parse_date(line_str: str) -> datetime | None:
        """
        Parses a string with or without time
        Returns a datetime object if the string is valid
        """
        match_time = re.search(r"(\w{3})\s+(\d{1,2})\s+(\d{2}:\d{2})", line_str)
        match_no_time = re.search(r"(\w{3})\s+(\d{1,2})\s+(\d{4})", line_str)

        if match_time:
            # Case with time
            month, day, time = match_time.groups()
            year = datetime.now().year
            return datetime.strptime(f"{month} {day} {time} {year}", "%b %d %H:%M %Y")
        elif match_no_time:
            # Case without time
            month, day, year = match_no_time.groups()
            return datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
        return None


class System:
    """
    Manages system-related operations like file and folder size handling
    """

    @staticmethod
    def get_size(folder_path: str) -> float:
        """
        Returns the size of a folder or file in GB
        """
        if os.path.isfile(folder_path):
            return round(os.path.getsize(folder_path) / (1024**3), 2)
        else:
            total_size = 0
            for dirpath, _, filenames in os.walk(folder_path):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    if not os.path.islink(file_path):
                        total_size += os.path.getsize(file_path)
            return round(total_size / (1024**3), 2)
