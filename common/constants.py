# -*- coding: utf-8 -*-

language_dict = {
    "IT": "Italian",
    "ES": "Spanish",
    "DE": "German",
    "FR": "French",
    "EN": "English",
    "TR": "Turkish",
    "PT": "Portuguese",
    "JA": "Japanese",
    "BG": "Bulgarian"
}


def my_language(iso639_1: str):
    return language_dict.get(iso639_1.upper(), '')
