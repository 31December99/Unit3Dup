# -*- coding: utf-8 -*-
import argparse

from common.external_services.igdb.core.models.search import Game
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.pvtDocu import PdfImages
from unit3dup.pvtVideo import Video
from dataclasses import dataclass
from unit3dup.media import Media



@dataclass
class Payload:
    tracker_name: str
    cli: argparse
    show_id: int | None
    imdb_id: int | None
    show_keywords: str | None
    video_info: Video | None
    igdb: Game | None
    docu_info: PdfImages | None


@dataclass
class BittorrentData:
    tracker_response: str | None
    torrent_response: Mytorrent | None
    content: Media
    tracker_message: dict | None
    archive_path: str
    payload: Payload | None



