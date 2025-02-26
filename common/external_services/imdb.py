# -*- coding: utf-8 -*-

from imdb import Cinemagoer
from common.utility import ManageTitles


class IMDB:

    show = {
        1: "movie",
        2: "tv",
    }

    def __init__(self):
        self.api = Cinemagoer()

    def search(self, query: str)-> int | None:
        movies = self.api.search_movie(query)
        for movie in movies:
            if ManageTitles.fuzzyit(str1=query, str2=movie.data['title']) > 95:
                return movie.movieID
