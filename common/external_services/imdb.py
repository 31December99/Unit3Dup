# -*- coding: utf-8 -*-

from imdb import Cinemagoer # Installato da github , su pipy non ancora disponibile la versione 2025
from view import custom_console
from rich.table import Table
from rich.align import Align

from common.utility import ManageTitles
from common import title


class IMDB:

    def __init__(self):
        self.api = Cinemagoer()

    def search(self, query: str)-> int | None:
        # Search for a tv or movie
        movies = self.api.search_movie(query)
        for movie in movies:
            if ManageTitles.fuzzyit(str1=query, str2=movie.data['title']) > 95:
                return movie.movieID

