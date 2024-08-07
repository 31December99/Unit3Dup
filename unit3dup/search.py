# -*- coding: utf-8 -*-
import sys

from unit3dup import tmdb, title
from rich.console import Console

console = Console(log_path=False)


class TvShow:

    def __init__(self, category: int):
        super().__init__()
        self.titles = None
        show = {
            1: "Movie",
            2: "Serie",
        }
        self.mytmdb = tmdb.MyTmdb(show[category])

    def start(self, file_name: str):
        guess_filename = title.Guessit(file_name)
        _title = guess_filename.guessit_title
        _alternate_title = guess_filename.guessit_alternative
        result = self.mytmdb.search(_title)

        # Se non ci sono risultati prima di richiedere all'utente provo ad unire il  main title con l'alternative title
        if not result:
            new_title = " ".join([_title, _alternate_title])
            result = self.mytmdb.search(new_title)
            if not result:
                result = self.mytmdb.input_tmdb()

        if result:
            backdrop_path = result.backdrop_path
            poster_path = result.poster_path
            overview = result.overview
            url_backdrop = (
                f"https://www.themoviedb.org/t/p/original{backdrop_path}"
                if backdrop_path
                else "nourl"
            )
            url_poster = (
                f"https://www.themoviedb.org/t/p/original{poster_path}"
                if poster_path
                else "nourl"
            )
            console.log(f"\n[TMDB ID]................  {result.video_id}")
            console.log(f"[TMDB POSTER]............  {url_poster}")
            console.log(f"[TMDB BACKDROP]..........  {url_backdrop}")
            console.log(f"[TMDB KEYWORDS]..........  {result.keywords}\n")
            return result
        else:
            console.log(f"Non trovo un ID valido per {file_name}")
            sys.exit()
