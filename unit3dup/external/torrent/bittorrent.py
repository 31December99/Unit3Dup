# -*- coding: utf-8 -*-

from dataclasses import dataclass
from unit3dup.external.media import Media


@dataclass
class BittorrentData:
    tracker_response: str
    content: Media
    tracker_message: dict
    archive_path: str
