# -*- coding: utf-8 -*-
import os
import re
import unicodedata

from datetime import datetime
from thefuzz import fuzz

from common.external_services.igdb.core.tags import (
    additions,
)

class ManageTitles:
    """
    Manages file title operations like removing punctuation,
    removing accented letters, and handling file types
    """

    marks = [
        ".", ",", ";", ":", "!", "?", '"', "(", ")", "[", "]", "{", "}", "/",
        "\\", "&", "*", "$", "%", "#", "@", "_", "+", "|"
    ]

    # TAG Audio in title
    iso_3166_alpha3= [ "ENG", "USA","ITA", "DEU",  "FRA",  "GBR", "ESP", "JPN", "BRA", "RUS", "CHN"]

    # TAG Audio in title
    iso_3166_alpha2_to_alpha3 = {
        "EN": "ENG",  # exception
        "US": "USA",
        "IT": "ITA",
        "DE": "DEU",
        "FR": "FRA",
        "GB": "GBR",
        "ES": "ESP",
        "JP": "JPN",
        "BR": "BRA",
        "RU": "RUS",
        "CN": "CHN",
    }

    @staticmethod
    def convert_iso(code)-> list | None:
        """ Convert iso 2 to 3 """
        code = code.upper()

        # if it's 'multilang'
        if '-' in code:
            codes = code.split('-')
        else:
            codes = [code]

        result = []
        for part in codes:
            # Capture the 2 or 3 letter code followed by '-' or end string
            match = re.match(r'([A-Za-z]{2,3})(?:-|$)', part)
            if match:
                iso_code = match.group(1)
                if len(iso_code) == 2:  # // alpha-2
                    return ManageTitles.iso_3166_alpha2_to_alpha3.get(code, None)
                elif len(iso_code) == 3:  # // alpha3
                    # return the same code provided it is an alpha3
                    if iso_code in ManageTitles.iso_3166_alpha3:
                        if iso_code:
                            result.append(iso_code)
        return result


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
    def remove_accent(my_string: str)-> str:
        """
        Removes accented characters from a string
        """
        str_tmp = unicodedata.normalize('NFD', my_string)
        return ''.join(char for char in str_tmp if unicodedata.category(char) != 'Mn')

    @staticmethod
    def filter_ext(file: str) -> bool:
        """
        Filters files by their extensions
        Returns True if the file is a video
        """
        video_ext = [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".ogg", 
            ".mpg", ".mpeg", ".m4v", ".rm", ".rmvb", ".vob", ".ts", ".m2ts", ".divx", 
            ".asf", ".swf", ".ogv", ".drc", ".m3u8", ".pdf", ".epub", ".rar"
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
    def media_docu_type(file_name: str) -> str | None:
        """
        Returns document type based on file extension
        """
        ext = os.path.splitext(file_name)[1].lower()
        type_ = {
            ".pdf": "edicola",
            ".epub": "edicola",
            }
        return type_.get(ext, None)

    @staticmethod
    def fuzzyit(str1: str, str2: str) -> int:
        """
        Returns similarity score between two strings
        """
        str2 = str2.lower().replace("-", "")
        str2 = ManageTitles.clean(str2)
        return fuzz.ratio(ManageTitles.remove_accent(str1.lower()), ManageTitles.remove_accent(str2.lower()))

    @staticmethod
    def normalize_filename(filename)-> str:
        # Remove spaces
        filename = filename.strip()

        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        # Normalize
        filename = unicodedata.normalize('NFD', filename).encode('ascii', 'ignore').decode('ascii')

        # Replace spaces with underscores
        filename = filename.replace(' ', '_')

        # Set file name length to 100 characters
        filename = filename[:100]

        # Remove periods or spaces at the end
        filename = filename.rstrip('. ')

        return filename

    @staticmethod
    def clean_text(filename: str)-> str:

        # Remove each addition from the string
        filename_sanitized = filename
        for addition in additions:
            filename_sanitized = re.sub(rf"\b{addition}\b", "", filename_sanitized)

        # Remove v version
        filename_sanitized = re.sub(r"v\d+(?:[ .]\d+)*", "", filename_sanitized).strip()

        # Remove dots, extra spaces
        filename_sanitized = re.sub(r"[._]", " ", filename_sanitized)

        # remove spaces, tab, newline
        filename_sanitized = re.sub(r"\s+", " ", filename_sanitized)

        # Recover tag
        filename_sanitized = ManageTitles.recover_tag(filename_sanitized)

        # remove double space
        filename_sanitized = re.sub(r"\s+", " ", filename_sanitized).strip()

        return filename_sanitized

    @staticmethod
    def recover_tag(filename_sanitized: str) -> str:

        # Add the tag
        replacements = [
            (r'\b7 \b1\b', '7.1'),
            (r'\b5 \b1\b', '5.1'),
            (r'\bDDP5 \b1\b', 'DDP5.1'),
            (r'\b2 \b0\b', '2.0'),
            (r'\bWEB \bDL\b', 'WEB-DL'),
            (r'\bWEB \bDLMUX\b', 'WEB-DLMUX'),
            (r'\bBD \bUNTOUCHED\b', 'BD-UNTOUCHED'),
            (r'\bCINEMA \bMD\b', 'CINEMA-MD'),
            (r'\bHEVC \bFHC\b', 'HEVC-FHC'),

        ]

        for tag, replacement in replacements:
            filename_sanitized = re.sub(tag, replacement, filename_sanitized, flags=re.IGNORECASE)
        return filename_sanitized




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

    # // Category neutral value before being translated into tracker values
    DOCUMENTARY = 4
    TV_SHOW = 2
    MOVIE = 1
    GAME = 3

    category_list = {MOVIE: 'movie', TV_SHOW: 'tv', GAME : 'game', DOCUMENTARY: 'edicola'}

    RESOLUTIONS= [ "8640", "4320",  "2160", "1080", "720", "576", "480"]
    RESOLUTION_labels = ["8640p", "4320p", "2160p", "1080p", "1080i", "720p", "720i", "576p", "576i", "480p", "480i"]
    NO_RESOLUTION = 'altro'

    @staticmethod
    def get_size(folder_path: str) -> (float, str):
        """
        Returns the size of a folder or file in GB or MB
        """
        if os.path.isfile(folder_path):
            total_size = os.path.getsize(folder_path)
        else:
            total_size = 0
            for dir_path, _, filenames in os.walk(folder_path):
                for file in filenames:
                    file_path = os.path.join(dir_path, file)
                    if not os.path.islink(file_path):
                        total_size += os.path.getsize(file_path)

        return (round(total_size / (1024 ** 3), 2), 'GB') if total_size > 1024 ** 3\
            else (round(total_size / (1024 ** 2), 2), 'MB')


