# -*- coding: utf-8 -*-
from unit3dup import tmdb, title


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
            url_backdrop = f"https://www.themoviedb.org/t/p/original{backdrop_path}" if backdrop_path else 'nourl'
            url_poster = f"https://www.themoviedb.org/t/p/original{poster_path}" if poster_path else 'nourl'
            print(f"[TMDB ID]................  {result.video_id}")
            print(f"[TMDB POSTER]............  {url_poster}")
            print(f"[TMDB BACKDROP]..........  {url_backdrop}")
            print(f"[TMDB KEYWORDS]..........  {result.keywords}\n")
            return result
