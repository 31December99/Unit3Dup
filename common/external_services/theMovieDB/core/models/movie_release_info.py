# -*- coding: utf-8 -*-


from dataclasses import dataclass, field


@dataclass
class MovieReleaseInfo:
    """
    Represents release information for a movie in a specific country.
    """
    iso_3166_1: str | None = None
    release_dates: dict[str, str] | None = field(default_factory=dict)

    def __repr__(self):
        """Returns a string representation"""
        return f"<ReleaseInfo iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"
