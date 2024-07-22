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
        return self.guessit.get('film_title', self.guessit.get('title', self.filename))

    @property
    def guessit_alternative(self):
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        return self.guessit.get('alternative_title', self.guessit.get('title', self.filename))

    @property
    def guessit_year(self):
        """
        Estrae l'anno di pubblicazione dal titolo
        :return:
        """
        return self.guessit['year'] if 'year' in self.guessit else None

    @property
    def guessit_episode(self):
        """
        Estrae il numero di episodio dal titolo
        :return:
        """
        return self.guessit['episode'] if 'episode' in self.guessit else None

    @property
    def guessit_season(self):
        """
        Estrae il numero di stagione dal titolo
        :return:
        """
        # return int(self.guessit['season']) if 'season' in self.guessit else None
        return self.guessit['season'] if 'season' in self.guessit else None

    @property
    def type(self):
        """
        Determina se è una serie verificando la presenza di un numero di stagione
        :return:
        """
        return self.guessit['type'] if 'type' in self.guessit else None
