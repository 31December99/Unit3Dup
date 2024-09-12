# -*- coding: utf-8 -*-

from .itt import itt_data
from dataclasses import dataclass
from common.utility.utility import Manage_titles


@dataclass
class ITTData:
    category: dict[str, str]
    freelech: dict[str, int]
    type_id: dict[str, str]
    resolution: dict[str, int]
    codec: list

    @classmethod
    def load_from_module(cls) -> "ITTData":
        """
        Carica i dati da un modulo e crea un'istanza di ITTData.
        """
        return cls(
            category=itt_data.get('CATEGORY'),
            freelech=itt_data.get('FREELECH'),
            type_id=itt_data.get('TYPE_ID'),
            resolution=itt_data.get('RESOLUTION'),
            codec=itt_data.get('CODEC'),
        )

    def filter_type(self, file_name: str) -> int:

        file_name = Manage_titles.clean(file_name)
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

    def filter_resolution(self, file_name: str) -> int:

        file_name = Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")
        for word in word_list:
            if word in self.resolution:
                return self.resolution[word]

        return -1
