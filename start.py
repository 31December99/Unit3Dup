# -*- coding: utf-8 -*-
import argparse
from unit3dup.uploader import Bot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands', add_help=False)
    parser.add_argument('-serie', '--serie', nargs=1, type=str, help='Serie')
    parser.add_argument('-movie', '--movie', nargs=1, type=str, help='Movie')
    args = parser.parse_args()

    bot = Bot(args=args)

