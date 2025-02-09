# -*- coding: utf-8 -*-

from dataclasses import dataclass
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents

@dataclass
class QBittorrent:
    tracker_response: str
    torrent_response: Mytorrent
    content: Contents
    tracker_message: dict
