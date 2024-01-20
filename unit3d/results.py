# -*- coding: utf-8 -*-
class Results:

    def __init__(self):
        self.__genre_ids = None
        self.__popularity = None
        self.__overview = None
        self.__result = None
        self.__id = 0
        self.__title_alternative = []
        self.__iso = []
        self.__poster_path = []
        self.__backdrop_path = []
        self.__genres_id = None
        self.__title = None
        self.__original_title = None
        self.__date = None
        self.__not_resources = False
        self.__keywords = False

    @property
    def backdrop_path(self) -> list:
        return self.__backdrop_path

    @property
    def poster_path(self) -> list:
        return self.__poster_path

    @property
    def popularity(self) -> list:
        return self.__popularity

    @property
    def video_id(self):
        return self.__id

    @property
    def translations(self):
        return self.__iso

    @property
    def alternative(self):
        return self.__title_alternative

    @property
    def genre_ids(self):
        return self.__genre_ids

    @property
    def overview(self):
        return self.__overview

    @property
    def original_title(self):
        return self.__original_title

    @property
    def title(self):
        return self.__title

    @property
    def date(self):
        return self.__date

    @property
    def not_resources(self):
        return self.__not_resources

    @property
    def keywords(self):
        return self.__keywords

    """
    SETTER
    """

    @backdrop_path.setter
    def backdrop_path(self, value):
        self.__backdrop_path = value

    @poster_path.setter
    def poster_path(self, value):
        self.__poster_path = value

    @popularity.setter
    def popularity(self, value):
        self.__popularity = value

    @video_id.setter
    def video_id(self, value):
        self.__id = value

    @translations.setter
    def translations(self, value):
        self.__iso = value

    @alternative.setter
    def alternative(self, value):
        self.__title_alternative = value

    @genre_ids.setter
    def genre_ids(self, value):
        self.__genre_ids = value

    @overview.setter
    def overview(self, value):
        self.__overview = value

    @original_title.setter
    def original_title(self, value):
        self.__original_title = value

    @title.setter
    def title(self, value):
        self.__title = value

    @date.setter
    def date(self, value):
        self.__date = value

    @not_resources.setter
    def not_resources(self, value):
        self.__not_resources = value

    @keywords.setter
    def keywords(self, value):
        self.__keywords = value
