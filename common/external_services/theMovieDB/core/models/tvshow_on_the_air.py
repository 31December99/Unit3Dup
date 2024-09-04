# -*- coding: utf-8 -*-
class OnTheAir:
    """
    Represents a TV show with various attributes.
    """

    def __init__(
            self,
            adult=None,
            backdrop_path=None,
            genre_ids=None,
            id=None,
            original_language=None,
            original_title=None,
            overview=None,
            popularity=None,
            poster_path=None,
            release_date=None,
            title=None,
            video=None,
            vote_average=None,
            vote_count=None,
            origin_country=None,
            original_name=None,
            first_air_date=None,
            name=None,
    ):
        """
        Initializes a TvShow instance with provided attributes.
        """
        self.adult = adult
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.id = id
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.title = title
        self.video = video
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.origin_country = origin_country
        self.original_name = original_name
        self.first_air_date = first_air_date
        self.name = name

    def __repr__(self):
        """Returns a string representation"""
        return f"<OnTheAir title={self.name} id={self.id}>"
