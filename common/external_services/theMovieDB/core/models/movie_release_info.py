# -*- coding: utf-8 -*-


class MovieReleaseInfo:
    """
    Represents release information for a movie in a specific country.
    """

    def __init__(self, iso_3166_1=None, release_dates=None):
        """
        Initializes a ReleaseInfo instance with provided attributes.
        """
        self.iso_3166_1 = iso_3166_1
        self.release_dates = release_dates

    def __repr__(self):
        """Returns a string representation"""
        return f"<ReleaseInfo iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"

