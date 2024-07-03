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

    if args.upload:
        user_input = Cli(args=args, tracker=args.tracker)

        if user_input:
            bot = UploadBot(user_input.content)
            if user_input.content.category == user_input.serie:
                data = bot.serie_data()
            else:
                data = bot.movie_data()
            bot.process_data(data)

    else:
        print("Sintassi non valida o valore nullo. Controlla..")
        print(f"[-u] {args.upload}")
        print(f"[-t] {args.tracker}")
