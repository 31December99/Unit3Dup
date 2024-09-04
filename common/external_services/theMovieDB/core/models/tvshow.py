# -*- coding: utf-8 -*-

class TvShow:
    """
    Represents a TV show.
    """

    def __init__(self, id: int, name: str, first_air_date: str, overview: str,
                 popularity: float, vote_average: float, vote_count: int,
                 genre_ids: list[int], origin_country: list[str],
                 original_language: str, original_name: str,
                 backdrop_path: str = None, poster_path: str = None, adult: bool = False):
        """
        Args:
            id (int): Unique identifier for the TV show.
            name (str): Name of the TV show.
            first_air_date (str): Date when the TV show was first aired.
            overview (str): Overview or description of the TV show.
            popularity (float): Popularity index of the TV show.
            vote_average (float): Average rating of the TV show.
            vote_count (int): Total number of votes the TV show has received.
            genre_ids (list[int]): List of genre IDs associated with the TV show.
            origin_country (list[str]): List of countries where the TV show originated.
            original_language (str): Original language of the TV show.
            original_name (str): Original name of the TV show.
            backdrop_path (str, optional): Path to the backdrop image of the TV show.
            poster_path (str, optional): Path to the poster image of the TV show.
            adult (bool, optional): Indicates if the TV show is for adults only.
        """
        self.id = id
        self.name = name
        self.first_air_date = first_air_date
        self.overview = overview
        self.popularity = popularity
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.genre_ids = genre_ids
        self.origin_country = origin_country
        self.original_language = original_language
        self.original_name = original_name
        self.backdrop_path = backdrop_path
        self.poster_path = poster_path
        self.adult = adult

    def __repr__(self) -> str:
        """
        Provides a string representation of the TvShow object.

        Returns:
            str: A string representation of the TV show object.
        """
        return f"TvShow({self.id}, {self.name}, {self.first_air_date})"