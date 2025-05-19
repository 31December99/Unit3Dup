# -*- coding: utf-8 -*-

from dataclasses import dataclass
from common.utility import ManageTitles
from . import tracker_list

@dataclass
class TRACKData:
    category: dict[str, int]
    freelech: dict[str, int]
    type_id: dict[str, int]
    resolution: dict[str, int]
    codec: list

    @classmethod
    def load_from_module(cls, tracker_name: str) -> "TRACKData":
        """
        Load tracker data from module
        """
        tracker_data= tracker_list[tracker_name.upper()]

        return cls(
            category=tracker_data.get("CATEGORY"),
            freelech=tracker_data.get("FREELECH"),
            type_id=tracker_data.get("TYPE_ID"),
            resolution=tracker_data.get("RESOLUTION"),
            codec=tracker_data.get("CODEC"),
        )

    def filter_type(self, file_name: str) -> int:

        file_name = ManageTitles.clean(file_name)
        # Remove '-' from the releaser or unknown encoder
        file_name = file_name.replace("-", " ")
        word_list = file_name.lower().strip().split(" ")

        # Caso 1: Cerca un TYPE_ID nel nome del file
        for word in word_list:
            if word in self.type_id:
                return self.type_id[word]

        # Caso 2: Se non trova un TYPE_ID, cerca un codec e ritorna 'encode'
        for word in word_list:
            if word in self.codec:
                return self.type_id.get("encode", -1)
        return self.type_id.get("altro", -1)
