# -*- coding: utf-8 -*-

from imdb import Cinemagoer
from view import custom_console
from rich.table import Table
from rich.align import Align

from common.utility import ManageTitles
from common import title


class IMDB:

    def __init__(self):
        self.api = Cinemagoer()

    @staticmethod
    def view_results(imdb_results: list):

        table = Table(
            style="dim",
            title_style="bold yellow",
        )
        table.add_column("Index", style="violet", header_style="bold violet", justify="center")
        table.add_column("TITLES", style="blue", header_style="blue", justify="center")
        table.add_column("Category", style="blue", header_style="blue", justify="center")

        # Print a table to present the results
        for index, result in enumerate(imdb_results):
            table.add_row(
                str(index),
                str(result.data['title']),
                str(result.data['kind']),
            )

        custom_console.bot_log(Align.center(table))

    @staticmethod
    def select_result(results: list) -> int | None:
        if results:
            while True:
                result = custom_console.user_input_str("\nChoice a result to send to the tracker (Q=exit, S=skip)")
                if result.upper() == "Q":
                    exit(1)
                if result.upper() == "S":
                    return None
                if result.isdigit():
                    user_choice = int(result)
                    if 0 <= user_choice < len(results):
                       return user_choice


    def search(self, query: str)-> int | None:
        movies = self.api.search_movie(query)
        for movie in movies:
            if ManageTitles.fuzzyit(str1=query, str2=movie.data['title']) > 95:
                return movie.movieID

    def search_keyword(self, query: str)-> str | None:
        movies = self.api.search_movie(query)
        self.view_results(imdb_results=movies)
        if index:=self.select_result(results=movies) is not None:
            selected = movies[index]
            return title.Guessit(selected.data['title']).guessit_title
