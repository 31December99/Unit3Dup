# -*- coding: utf-8 -*-


from decouple import config
from unit3dup.uploader import Bot, trackers

TRACKER_NAME = config('TRACK_NAME')


if __name__ == "__main__":
    bot = Bot(trackers.get(TRACKER_NAME))
