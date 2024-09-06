from dataclasses import dataclass, field
from common.external_services import logger


@dataclass
class MovieReleaseInfo:
    """
    Represents release information for a movie in a specific country.
    """

    iso_3166_1: str | None = None
    release_dates: list[dict[str, any]] = field(default_factory=list)

    def __repr__(self) -> str:
        """
        Returns the MovieReleaseInfo string
        """
        return f"<ReleaseInfo iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"

    @classmethod
    def validate_data(cls, data: dict) -> 'MovieReleaseInfo | None':
        """
        Validates the data; return None if it's invalid
        """

        iso_3166_1 = data.get("iso_3166_1")
        release_dates = data.get("release_dates", {})

        # Validate country code
        if iso_3166_1 is not None:
            if (
                not isinstance(iso_3166_1, str)
                or len(iso_3166_1) != 2
                or not iso_3166_1.isupper()
            ):
                logger.error(f"Invalid ISO 3166-1 code: {iso_3166_1}")
                return None

            # Validate release_dates
        if not isinstance(release_dates, list):
            logger.error("release_dates must be a list.")
            return None

        for item in release_dates:
            if not isinstance(item, dict):
                logger.error(f"Invalid item in release_dates list: {item}")
                return None

        return cls(iso_3166_1=iso_3166_1, release_dates=release_dates)
