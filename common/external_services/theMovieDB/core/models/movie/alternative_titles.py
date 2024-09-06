# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from common.external_services import logger
import json


@dataclass
class Title:
    iso_3166_1: str
    title: str
    type: str | None = None
    logger: logger = field(init=False, repr=False)

    def __post_init__(self):
        """
        method invoked right after  the __init__ method !
        """
        self.logger = logger.getChild(self.__class__.__name__)

    @staticmethod
    def from_dict(data: dict[str, any]) -> "Title | None":
        try:
            return Title(
                iso_3166_1=data["iso_3166_1"],
                title=data["title"],
                type=data.get("type"),
            )
        except KeyError as e:
            logger.debug(f"Missing key in Title data: {e}")
            return None
        except TypeError as e:
            logger.debug(f"Type error in Title data: {e}")
            return None


@dataclass
class AltTitle:
    id: int
    titles: list[Title]

    @classmethod
    def from_json(cls, json_str: str) -> "AltTitle":
        data = json.loads(json_str)
        id_ = data.get("id", 0)
        titles_data = data.get("titles", [])
        titles = [
            Title.from_dict(title_data)
            for title_data in titles_data
            if Title.from_dict(title_data) is not None
        ]
        return cls(id=id_, titles=titles)
