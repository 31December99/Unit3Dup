# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.uploader import UploadBot
from unit3dup.contents import Cli

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
