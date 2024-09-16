# -*- coding: utf-8 -*-

from dataclasses import dataclass
import datetime


@dataclass
class FTPDirectory:
    permissions: str | None = None
    type: str | None = None
    links: int | None = None
    owner: str | None = None
    group: str | None = None
    size: int | None = None
    date: datetime.date | None = None
    time: datetime.time | None = None
    name: str | None = None
