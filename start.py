# -*- coding: utf-8 -*-
import argparse
from decouple import config
from unit3dup.uploader import Bot, trackers

TRACKER_NAME = config('TRACK_NAME')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands', add_help=False)
    parser.add_argument('-serie', '--serie', nargs=1, type=str, help='Serie')
    parser.add_argument('-movie', '--movie', nargs=1, type=str, help='Movie')
    args = parser.parse_args()

    bot = Bot(trackers.get(TRACKER_NAME), args=args)
