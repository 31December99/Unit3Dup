# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class Thumbnails:
    default: dict[str, int]
    high: dict[str, int]
    medium: dict[str, int]


@dataclass
class Snippet:
    channelId: str
    channelTitle: str
    description: str
    liveBroadcastContent: str
    publishTime: str
    publishedAt: str
    title: str
    thumbnails: Thumbnails


@dataclass
class Id:
    kind: str
    videoId: str


@dataclass
class Item:
    etag: str
    id: Id
    kind: str
    snippet: Snippet


@dataclass
class PageInfo:
    resultsPerPage: int
    totalResults: int


@dataclass
class YouTubeSearchResponse:
    etag: str
    items: list[Item]
    kind: str
    pageInfo: PageInfo
    regionCode: str

