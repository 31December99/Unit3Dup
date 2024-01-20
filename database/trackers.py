# -*- coding: utf-8 -*-

import utitlity


class Config:

    def filterType(self, file_name: str) -> int:
        pass

    def filterCodec(self, file_name: str) -> bool:
        pass

    def filterResolution(self, file_name: str) -> int:
        pass


class ITT(Config):
    category = {'movie': 1,
                'serie_tv': 2
                }

    def get_freelech(self, size: int) -> int:
        if size >= 20:
            return 100
        elif size >= 15:
            return 75
        elif size >= 10:
            return 50
        elif size >= 1:
            return 25
        else:
            return 0

    # alias format,source,type_id
    def filterType(self, file_name: str) -> int:
        """
        Cerca le keyword nel titolo
        Cerca eventuali codec nel titolo e lo setta come codice con il valore di ritorno
        :param file_name:
        :return:
        """
        file_name = utitlity.Manage_titles.clean(file_name)
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
        # if Manage_titles.filterCodec(file_name):
        if self.filterCodec(file_name):
            return type_dict['encode']  # encode
        return type_dict['altro']

    def filterCodec(self, file_name: str) -> bool:
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

    def filterResolution(self, file_name: str) -> int:
        file_name = utitlity.Manage_titles.clean(file_name)
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


class SHAISL(Config):
    category = {'movie': 1,
                'serie_tv': 2
                }

    def get_freelech(self, size: int) -> int:
        if size >= 20:
            return 100
        elif size >= 15:
            return 75
        elif size >= 10:
            return 50
        elif size >= 5:
            return 25
        else:
            return 0

    def filterType(self, file_name: str) -> int:
        """
        Cerca le keyword nel titolo
        Cerca eventuali codec nel titolo e lo setta come codice con il valore di ritorno
        :param file_name:
        :return:
        """
        file_name = utitlity.Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")
        type_dict = {
            "encode": 15,
            "web-dl": 27,
            "webdl": 29,
            "webrip": 7,
            "remux": 26,
            "full-disc": 33,
            "hdtv": 33,
            "cinamenews": 42,
            "windows": 31,
            "mac": 32,
            "android": 38,
            "linux": 39,
            "ios": 40,
            "mp3": 25,
            "flac": 24,
            "altro": 47,
        }

        for word in word_list:
            for key, value in type_dict.items():
                if word == key:
                    print(f"\n[TYPE]................  {word.upper()}\n")
                    return type_dict[word]

        # Se non trova la keyword 'codec' cerca eventuali nomi di codec
        # if Manage_titles.filterCodec(file_name):
        if self.filterCodec(file_name):
            return type_dict['encode']  # encode
        return type_dict['altro']

    def filterCodec(self, file_name: str) -> bool:
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

    def filterResolution(self, file_name: str) -> int:
        file_name = utitlity.Manage_titles.clean(file_name)
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
