# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Translation:
    """
    Represents a TV show translation
    """
    iso_639_1: str
    """
    Language code of the translation
    """
    english_name: str
    """
    English name of the language
    """
    name: str
    """
    Name of the translation
    """
    url: str | None
    """
    Optional URL associated with the translation
    """
    tagline: str | None
    """
    Optional tagline for the translation
    """
    description: str | None
    """
    Optional description for the translation
    """
    country: str | None
    """
    Optional country code related to the translation
    """


@dataclass
class TranslationsResponse:
    """
    Contains a list of TV show translations
    """
    translations: list[Translation]
    """
    List of Translation objects
    """
