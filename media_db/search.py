# -*- coding: utf-8 -*-
import sys

from media_db import tmdb
from common.utility import title
from common.config import config
from common.custom_console import custom_console
from common.external_services.trailers.api import YtTrailer
from unit3dup.contents import Contents



class TvShow:

    def __init__(self, content: Contents):
        super().__init__()
        self.titles = None
        self.content = content
        self.episode_title: str | None = None
        category = content.category

        show = {
            1: "Movie",
            2: "Serie",
        }
        self.mytmdb = tmdb.MyTmdb(table=show[category], content=content)

    def start(self, file_name: str):
        custom_console.bot_question_log(f"Processing '{file_name}'. Please wait...\n")

        guess_filename = title.Guessit(file_name)
        _title = guess_filename.guessit_title
        _alternate_title = guess_filename.guessit_alternative
        result = self.mytmdb.search(_title)
        # search episode title for the SxEx of the current content file_name or None if it's a movie
        self.episode_title = self.mytmdb.episode_title

        # Se non ci sono risultati prima di richiedere all'utente provo a unire il main title con l'alternative title
        if not result:
            new_title = " ".join([_title, _alternate_title])
            result = self.mytmdb.search(new_title)
            if not result:
                result = self.mytmdb.input_tmdb()

        if result:
            # Get the trailer link from the tmdb database
            result.trailer_key = self.trailer(video_id=result.video_id)
            # Get the trailer link from YouTube
            if not result.trailer_key:
                result.trailer_key = self.youtube_trailer(media=_title)

            backdrop_path = result.backdrop_path
            poster_path = result.poster_path
            url_backdrop = (
                f"https://www.themoviedb.org/t/p/original{backdrop_path}"
                if backdrop_path
                else "nourl"
            )
            result.backdrop_path = url_backdrop

            url_poster = (
                f"https://www.themoviedb.org/t/p/original{poster_path}"
                if poster_path
                else "nourl"
            )
            result.poster_path = url_poster

            custom_console.bot_log(f"\n[TMDB ID]................  {result.video_id}")
            custom_console.bot_log(f"[TMDB POSTER]............  {result.poster_path}")
            custom_console.bot_log(f"[TMDB BACKDROP]..........  {result.backdrop_path}")
            custom_console.bot_log(f"[TRAILER]................  https://www.youtube.com/watch?v={result.trailer_key}\n")

            return result
        else:
            custom_console.bot_log(f"Non trovo un ID valido per {file_name}")
            sys.exit()


    def trailer(self, video_id: int) -> str:
        self.mytmdb.tmdb.language='it'
        videos = self.mytmdb.tmdb.videos(video_id)
        if not videos['results']:
            self.mytmdb.tmdb.language = 'en'
            videos = self.mytmdb.tmdb.videos(video_id)

        trailer = next((video for video in videos['results'] if video['type'].lower() == 'trailer' and video['site'].lower() == 'youtube'), None)
        if trailer:
            return trailer['key']

    @staticmethod
    def youtube_trailer(media: str):

        custom_console.bot_question_log("TMDB trailer not found. Try searching on YouTube...\n")

        channel_id = None
        if config.YOUTUBE_CHANNEL_ENABLE:
            channel_id = config.YOUTUBE_CHANNEL_ID

        yt_trailer = YtTrailer(media)
        result = yt_trailer.get_trailer_link(channel_id)
        if result:
            custom_console.bot_question_log("Found !\n")
            return result[0].items[0].id.videoId
