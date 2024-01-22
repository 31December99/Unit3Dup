# -*- coding: utf-8 -*-
import argparse
import json
import os
import re

from unit3dup.uploader import UploadBot
from unit3dup import userinput


class Cli:

    def __init__(self, path: str, tracker: str, is_dir: bool):

        self.serie = 2
        self.movie = 1
        self.path = path
        self.tracker = tracker
        self.is_dir = is_dir

        # Se gli passi un file anche dentro una cartella basta che punti al file , lo considera un movie
        if not is_dir:
            # Qui non occorre utilizzare regex come nel caso di una folder
            self.file_name = os.path.basename(path)
            self.folder = os.path.dirname(path)
            self.category = 1
            self.name, ext = os.path.splitext(self.file_name)
            self.size = os.path.getsize(os.path.join(self.folder, self.file_name))
            metainfo_str = [{'length': self.size, 'path': [self.file_name]}]
            self.metainfo = json.dumps(metainfo_str, indent=4)

        if is_dir:
            list_dir = self.listdir()
            self.file_name = list_dir[0]
            self.folder = path
            self.category = 2
            self.name, ext = os.path.splitext(self.file_name)
            regex_pattern = r'(\sS\d{2}E\d{1,3}|\s\d{1,2}x\d{1,3})'
            # Elimino la parte SxEx per ottenere una stringa pulita che rappresenti il titolo
            self.name = re.sub(regex_pattern, '', self.name)

            if list_dir:
                self.metainfo_list = []
                for t in list_dir:
                    self.size = os.path.getsize(os.path.join(self.folder, t))
                    self.metainfo_list.append({'length': self.size, 'path': [t]})
            self.metainfo = json.dumps(self.metainfo_list, indent=4)

        self.content = userinput.Contents(file_name=self.file_name, folder=self.folder, name=self.name, size=self.size,
                                          metainfo=self.metainfo, category=self.category, tracker_name=tracker)

    def listdir(self):

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands', add_help=False)
    parser.add_argument('-u', '--upload', nargs=1, type=str, help='Upload Path')
    parser.add_argument('-t', '--tracker', nargs=1, type=str, help='Tracker Name')
    args = parser.parse_args()

    user_input = Cli(path=args.upload[0], tracker=args.tracker[0], is_dir=os.path.isdir(args.upload[0]))
    bot = UploadBot(user_input.content)
    if user_input.content.category == user_input.serie:
        data = bot.serie_data()
    else:
        data = bot.movie_data()
    bot.process_data(data)
