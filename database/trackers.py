# -*- coding: utf-8 -*-
import json
import os.path
from unit3dup import utility


class Filter:

    def filterType(self, file_name: str) -> int:
        pass

    def filterCodec(self, file_name: str) -> bool:
        pass

    def filterResolution(self, file_name: str) -> int:
        pass


class TrackerConfig(Filter):

    def __init__(self, config_file: str):
        if os.path.exists(config_file):
            # // Converto to json
            with open(config_file) as jsonfile:
                config = json.load(jsonfile)
            # // lower_case
            self.__config = {json_key: value for json_key, value in config.items()}

    def category(self, name: str) -> int:
        return self.__config["CATEGORY"][name]

    def type_id(self, name: str) -> str:
        dict_attribute = self.__config.get("TYPE_ID", {})
        return dict_attribute.get(name, "")

    def res_id(self, name: str) -> str:
        dict_attribute = self.__config.get("RESOLUTION", {})
        return dict_attribute.get(name, "")

        # return self.__config['RESOLUTION'][name]

    def filterType(self, file_name: str) -> int:
        """
        Divide il titolo in più parole
        Cerca eventuali codec nel titolo e lo setta come codice con il valore di ritorno
        :param file_name:
        :return:
        """
        file_name = utility.Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")

        # // 1 case
        for word in word_list:
            if word in self.__config["TYPE_ID"]:
                return int(self.__config["TYPE_ID"][word])

        # // 2 case
        # Se non trova un TYPE_ID cerca un eventuale codec
        for word in word_list:
            if word in self.__config["CODEC"]:
                return self.__config["TYPE_ID"]["encode"]
        return self.__config["TYPE_ID"]["altro"]

    def filterResolution(self, file_name: str) -> int:

        file_name = utility.Manage_titles.clean(file_name)
        word_list = file_name.lower().strip().split(" ")
        for word in word_list:
            if word in self.__config["RESOLUTION"]:
                return int(self.__config["RESOLUTION"][word])

    def get_freelech(self, size: int) -> int:
        if size >= 20:
            return self.__config["FREELECH"]["size20"]
        elif size >= 15:
            return self.__config["FREELECH"]["size15"]
        elif size >= 10:
            return self.__config["FREELECH"]["size10"]
        elif size >= 5:
            return self.__config["FREELECH"]["size5"]
        else:
            return 0
