# -*- coding: utf-8 -*-
from myTMDB import MyTmdb


class SearchTvShow:

    def __init__(self, videotype: str):
        super().__init__()
        self.titles = None
        self.mytmdb = MyTmdb(videotype)

    def start(self, title: str):
        result = self.mytmdb.search(title)
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