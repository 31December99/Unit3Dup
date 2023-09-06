#!/usr/bin/env python3.9
import json
import os
import sys


class Args:
    """
    Prepara i files per il torrent
    """

    def __init__(self, arg: list):

        self.tracker_file_name = None
        self.file_name = None
        self.base_name = None
        self.tracker_name = None
        self.path = None
        self.type = None
        self.arg = arg[0]

    def folder(self) -> str:
        # Solo percorso -
        if os.path.isdir(self.arg):
            print("Solo percorso")
            self.type = True
            self.path = self.arg
            self.base_name = os.path.basename(self.arg)
            # il primo in elenco come input a mediainfo
            dir_list = self.listdir()
            self.file_name = dir_list[0]
            metainfo = []
            for t in dir_list:
                size = os.path.getsize(os.path.join(self.path, t))
                metainfo.append({'length': size, 'path': [t]})

            print(json.dumps(metainfo, indent=4))
            print(self.base_name)
            print(self.file_name)
            print(self.path)

            return json.dumps(metainfo, indent=4)

    def file(self) -> str:
        # percorso + file_name
        if os.path.isfile(self.arg):
            print("Percorso + file /file")
            self.type = False
            self.file_name = os.path.basename(self.arg)
            self.base_name = None

            self.path = self.arg.replace(self.file_name, '')
            if os.path.exists(self.path):
                self.tracker_file_name, ext = os.path.splitext(self.file_name)
                size = os.path.getsize(os.path.join(self.path, self.file_name))
                metainfo = [{'length': size, 'path': [self.file_name]}]
                return json.dumps(metainfo, indent=4)
            #todo: path not exists
            else:
                print("Args: path not exists")
                input("premi un tasto per uscire")
                sys.exit()

    def listdir(self):
        """

        :return: ELenca solo i files con estensioni video
        """

        video_extensions = [
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
            ".mov",
            ".swf",
            ".mpg",
            ".mpeg",
            ".ogv",
            ".drc",
            ".m3u8"
        ]

        files_list = []
        for file in os.listdir(self.path):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in video_extensions:
                files_list.append(file)

        return files_list

    @property
    def fileName(self):
        return self.file_name

    @property
    def pathName(self):
        return self.path
