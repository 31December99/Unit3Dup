# -*- coding: utf-8 -*-
from unit3dup import tmdb, title
from rich.console import Console

console = Console(log_path=False)


class TvShow:

    def __init__(self, videotype: str):
        super().__init__()
        self.titles = None
        self.mytmdb = tmdb.MyTmdb(videotype)

    def start(self, file_name: str):
        _title = title.Guessit(file_name).guessit_title

        result = self.mytmdb.search(_title)
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
