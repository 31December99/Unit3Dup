# -*- coding: utf-8 -*-
import guessit


class Guessit:

    def __init__(self, filename: str):
        self.guessit = guessit.guessit(filename)
        self.filename = filename

    @property
    def guessit_title(self):
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
    def guessit_alternative(self):
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        return self.guessit.get(
            "alternative_title", self.guessit.get("title", self.filename)
        )

    @property
    def guessit_year(self):
        """
        Estrae l'anno di pubblicazione dal titolo
        :return:
        """
        return self.guessit["year"] if "year" in self.guessit else None

    @property
    def guessit_episode(self):
        """
        Estrae il numero di episodio dal titolo
        :return:
        """
        return self.guessit["episode"] if "episode" in self.guessit else None

    @property
    def guessit_season(self):
        """
        Estrae il numero di stagione dal titolo
        :return:
        """
        # return int(self.guessit['season']) if 'season' in self.guessit else None
        return self.guessit["season"] if "season" in self.guessit else None

    @property
    def guessit_episode_title(self):
        """
        Get the episode title
        :return:
        """
        return self.guessit["episode_title"] if "episode_title" in self.guessit else None

    @property
    def type(self):
        """
        Determina se è una serie verificando la presenza di un numero di stagione
        :return:
        """
        return self.guessit["type"] if "type" in self.guessit else None

    @property
    def source(self):
        """
        Grab the source
        :return:
        """
        return self.guessit["source"] if "source" in self.guessit else None

    @property
    def other(self):
        """
        Grab the 'other' info
        :return:
        """
        return self.guessit["other"] if "other" in self.guessit else None

    @property
    def audio_codec(self):
        """
        Grab the 'other' info
        :return:
        """
        return self.guessit["audio_codec"] if "audio_codec" in self.guessit else None

    @property
    def subtitle(self):
        """
        Grab the 'other' subtitle
        :return:
        """
        return self.guessit["subtitle"] if "subtitle" in self.guessit else None

    @property
    def release_group(self):
        """
        Grab the 'release_group'
        :return:
        """
        return (
            self.guessit["release_group"] if "release_group" in self.guessit else None
        )

    @property
    def screen_size(self):
        """
        Grab the 'screen_size'
        :return:
        """
        return self.guessit["screen_size"] if "screen_size" in self.guessit else None
