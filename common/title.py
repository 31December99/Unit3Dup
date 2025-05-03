# -*- coding: utf-8 -*-
import guessit
from common.utility import ManageTitles


class Guessit:

    def __init__(self, filename: str):
        temp_name = ManageTitles.replace(filename)
        self.guessit = guessit.guessit(temp_name)
        self.filename = filename

    @property
    def guessit_title(self) -> str:
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        #
        # Se fallisce guessit ad esempio in questo caso :
        # titolo : 1923 ( nessun altra informazione nel titolo)
        # MatchesDict([('year', 1923), ('type', 'movie')])
        # dove non trova ne title e film_title e erroneamente lo credo un movie..
        # bypass guessit e ritorna filename alla ricerca di tmdb
        return self.guessit.get("film_title", self.guessit.get("title", self.filename))

    @property
    def guessit_alternative(self) -> str:
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        return self.guessit.get(
            "alternative_title", self.guessit.get("title", self.filename)
        )

    @property
    def guessit_year(self) -> str | None:
        """
        Estrae l'anno di pubblicazione dal titolo
        :return:
        """
        return self.guessit["year"] if "year" in self.guessit else None

    @property
    def guessit_episode(self) -> str | None:
        """
        Estrae il numero di episodio dal titolo
        :return:
        """
        return self.guessit["episode"] if "episode" in self.guessit else None

    @property
    def guessit_season(self) -> str | None:
        """
        Estrae il numero di stagione dal titolo
        :return:
        """
        # return int(self.guessit['season']) if 'season' in self.guessit else None
        return self.guessit["season"] if "season" in self.guessit else None

    @property
    def guessit_episode_title(self) -> str:
        """
        Get the episode title
        :return:
        """
        return guessit.guessit(self.filename, {"excludes": "part"}).get("episode_title", "")


    @property
    def type(self) -> str | None:
        """
        Determina se è una serie verificando la presenza di un numero di stagione
        :return:
        """
        return self.guessit["type"] if "type" in self.guessit else None

    @property
    def source(self) -> str | None:
        """
        Grab the source
        :return:
        """
        return self.guessit["source"] if "source" in self.guessit else None

    @property
    def other(self) -> str | None:
        """
        Grab the 'other' info
        :return:
        """
        return self.guessit["other"] if "other" in self.guessit else None

    @property
    def audio_codec(self) -> str | None:
        """
        Grab the 'other' info
        :return:
        """
        return self.guessit["audio_codec"] if "audio_codec" in self.guessit else None

    @property
    def subtitle(self) -> str | None:
        """
        Grab the 'other' subtitle
        :return:
        """
        return self.guessit["subtitle"] if "subtitle" in self.guessit else None

    @property
    def release_group(self) -> str | None:
        """
        Grab the 'release_group'
        :return:
        """
        return (
            self.guessit["release_group"] if "release_group" in self.guessit else None
        )

    @property
    def screen_size(self) -> str | None:
        """
        Grab the 'screen_size'
        :return:
        """
        return self.guessit["screen_size"] if "screen_size" in self.guessit else None
