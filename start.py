# -*- coding: utf-8 -*-
import argparse
from unit3dup.uploader import UploadBot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands', add_help=False)
    parser.add_argument('-s', '--serie', nargs=1, type=str, help='Serie')
    parser.add_argument('-m', '--movie', nargs=1, type=str, help='Movie')
    parser.add_argument('-t', '--tracker', nargs=1, type=str, help='Tracker Name')
    args = parser.parse_args()

    bot = UploadBot(args=args)
