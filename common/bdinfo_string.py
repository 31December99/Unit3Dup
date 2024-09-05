# -*- coding: utf-8 -*-

class BDInfo:
    """
    A class to represent information about a Blu-ray disc.

    Attributes:
        disc_label (str): The label or name of the disc.
        disc_size (str): The size of the disc.
        protection (str): The type of protection applied to the disc.
        playlist (str): The playlist information.
        size (str): The size of the content on the disc.
        length (str): The length of the content on the disc.
        total_bitrate (str): The total bitrate of the disc content.
        video (str): The video specifications.
        audio (list[str]): A list of audio specifications.
        languages (list[str]): A list of languages extracted from audio specifications.
        subtitles (list[str]): A list of subtitle specifications.

    Methods:
        from_bdinfo_string(bd_info_string: str) -> 'BDInfo':
            Creates an instance of BDInfo from a formatted string.
    """

    def __init__(
        self,
        disc_label: str,
        disc_size: str,
        protection: str,
        playlist: str,
        size: str,
        length: str,
        total_bitrate: str,
        video: str,
        audio: list[str],
        languages: list[str],
        subtitles: list[str],
    ):
        self.disc_label = disc_label
        self.disc_size = disc_size
        self.protection = protection
        self.playlist = playlist
        self.size = size
        self.length = length
        self.total_bitrate = total_bitrate
        self.video = video
        self.audio = audio
        self.languages = languages
        self.subtitles = subtitles

    @classmethod
    def from_bdinfo_string(cls, bd_info_string: str) -> 'BDInfo':
        """
        Creates an instance of BDInfo from a formatted string.

        Args:
            bd_info_string (str): A string containing Blu-ray disc information formatted with labels and values.

        Returns:
            BDInfo: An instance of the BDInfo class with attributes populated from the input string.
        """
        lines = bd_info_string.strip().split("\n")
        data = {"audio": [], "subtitles": []}

        for line in lines:
            # Parsing Audio
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip().replace(" ", "_").lower()

                if key == "audio":
                    data["audio"].append(value.strip().lower())
                elif key == "subtitle":
                    data["subtitles"].append(value.strip().lower())
                else:
                    data[key] = value.strip()

        # Parsing Languages
        languages_parsed = []
        for item in data["audio"]:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.split("/")
            languages_parsed.append(item[0].strip())

        return cls(
            disc_label=data.get("disc_label"),
            disc_size=data.get("disc_size"),
            protection=data.get("protection"),
            playlist=data.get("playlist"),
            size=data.get("size"),
            length=data.get("length"),
            total_bitrate=data.get("total_bitrate"),
            video=data.get("video"),
            audio=data["audio"],
            languages=languages_parsed,
            subtitles=data["subtitles"],
        )
