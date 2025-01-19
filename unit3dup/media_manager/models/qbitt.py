# -*- coding: utf-8 -*-

import requests

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents
from dataclasses import dataclass


@dataclass
class QBittorrent:
    tracker_response: str
    torrent_response: Mytorrent
    content: Contents
    tracker_message: dict
