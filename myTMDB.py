#!/usr/bin/env python3.9
import sys
from datetime import datetime

import fasttext
import guessit
import utitlity
from decouple import config
from tmdbv3api import TMDb, Movie, TV

TMDB_APIKEY = config('TMDB_APIKEY')


class Myguessit:

    def __init__(self, filename: str):
        self.guessit = guessit.guessit(filename)

    @property
    def guessit_title(self):
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        return self.guessit['film_title'] if 'film_title' in self.guessit else self.guessit['title']

    @property
    def guessit_alternative(self):
        """
        Estrae la stringa con il titolo dal nome del file film_title o title(serie ?)
        :return:
        """
        return self.guessit['alternative_title'] if 'alternative_title' in self.guessit else self.guessit['title']

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
        return self.guessit['episode'] if 'episode' in self.guessit else 0

    @property
    def guessit_season(self):
        """
        Estrae il numero di stagione dal titolo
        :return:
        """
        return self.guessit['season'] if 'season' in self.guessit else 0

    @property
    def type(self):
        """
        Determina se è una serie verificando la presenza di un numero di stagione
        :return:
        """
        return self.guessit['type'] if 'type' in self.guessit else None

    @property
    def is_movie(self):
        """
        Determina se è un movie varificando la presenza diu numero di stagione
        :return:
        """
        return True if not self.season else False


class TmdbMovie:

    def __init__(self, myguessit: Myguessit):

        # TMDB
        self.tmdb = TMDb()
        self.tmdb.api_key = TMDB_APIKEY
        self.tmdb.language = 'it'
        self.tmdb.debug = True
        self.mv_tmdb = Movie()
        self.result = None
        self.myguessit = myguessit

        self.myguessit.guessit_title.lower()

    def _search(self, attributo: str) -> list:

        """
        Determina se cercare in movies o series ( Vale per TMDB)
        :param attributo:
        :return:
        """
        self.result = self.mv_tmdb.search(self.myguessit.guessit_title)
        """
        Cerca nei risultati con l'attributo scelto es: 'title' e ritorna una lista  
        """
        return [(item[attributo], item['id'], datetime.strptime(item['release_date'], '%Y-%m-%d').year)
                for item in self.result if item['release_date']]

    @property
    def confronto(self) -> list:
        """
        un elenco di chiamate API per svolgere le funzioni principali
        :return: ritorna il titolo con lo stesso anno di uscita e titolo identico
        elimina ogni carattere di punteggiatura in title e in title tmdb
        """
        candidate = self._search('title')
        return [(title, video_id, year) for title, video_id, year in candidate if year == self.myguessit.guessit_year
                and utitlity.Manage_titles.clean(title.lower()) ==
                utitlity.Manage_titles.clean(self.myguessit.guessit_title.lower())]

    @property
    def adult(self):
        return self._search('adult')

    @property
    def backdrop_path(self):
        return self._search('backdrop_path')

    @property
    def genre_ids(self):
        return self._search('genre_ids')

    @property
    def video_id(self):
        return self._search('id')

    @property
    def original_language(self):
        return self._search('original_language')

    @property
    def overview(self):
        return self._search('overview')

    @property
    def popularity(self):
        return self._search('popularity')

    @property
    def poster_path(self):
        return self._search('poster_path')

    @property
    def vote_average(self):
        return self._search('vote_average')

    @property
    def vote_count(self):
        return self._search('vote_count')

    @property
    def title(self) -> list:
        return self._search('title')

    @property
    def original_title(self):
        return self._search('original_title')

    @property
    def release_date(self):
        return self._search('release_date')

    @property
    def translations(self):
        details = self.mv_tmdb.details(self.video_id)
        if getattr(details, 'tagline', False):
            return [r['data']['title'] for r in details['translations']['translations']]

    @property
    def details(self):
        """
        Creo una lista di dizionari dove viene riportato per ogni dizionario titolo tradotto,tagline,videoid
        :return:
        """
        details_dictionary_list = []
        for title, video_id, year in self.video_id:
            details = self.mv_tmdb.details(video_id)

            if getattr(details, 'translations', False):
                details_list = [({"title_key": t['data']['title'], "tagline_value": t['data']['tagline'],
                                  "video_id": video_id})
                                for t in details['translations']['translations'] if t['data']['title']]
                details_dictionary_list.append(details_list)
        return details_dictionary_list

    def cerca(self):
        if not self.confronto:
            for det in self.details:
                for det2 in det:
                    if (utitlity.Manage_titles.clean(self.myguessit.guessit_alternative.lower()) in
                            utitlity.Manage_titles.clean(det2['title_key'].lower())):
                        if (utitlity.Manage_titles.clean(self.myguessit.guessit_title.lower()) in
                                utitlity.Manage_titles.clean(det2['title_key'].lower())):
                            return det2['video_id']
        else:
            return self.confronto[0][1]


class TmdbSeries:
    def __init__(self, myguessit: Myguessit):

        # TMDB
        # todo: rimuovere i ':' dal file_name e dal name in tmdb poi confrontare
        # todo: rimuovere il confronto con la data in serie se non disponibile da field_name

        """
         anche se il risultato delle ricerca commuta la lingua non posso fare il confronto con due lingue
         diverse

        :param myguessit:
        """
        self.myguessit = myguessit
        # https://github.com/facebookresearch/fastText/issues/1067#issue-617428110
        fasttext.FastText.eprint = lambda x: None
        self.model = fasttext.load_model("lid.176.bin")
        self.predict_lang = self.model.predict(self.myguessit.guessit_title, k=3)
        self.lang = self.predict_lang[0][0].split('__label__')[1].replace('en', 'us')
        self.tmdb = TMDb()
        self.tmdb.api_key = TMDB_APIKEY
        self.tmdb.language = self.lang
        self.tmdb.debug = True
        self.tv_tmdb = TV()
        self.result = None

    def _search(self, attributo: str) -> list:

        """
        Determina se cercare in movies o series ( Vale per TMDB)
        :param attributo:
        :return:
        """

        self.result = self.tv_tmdb.search(self.myguessit.guessit_title)
        if not self.result['results']:
            utitlity.Console.print("La cartella non sembra contenere una serie tv..Verifica", 1)
            sys.exit()

        """
        Cerca nei risultati con l'attributo scelto es: 'title' e ritorna una lista  
        """

        return [(item[attributo], item['id'], datetime.strptime(item['first_air_date'],
                                                                '%Y-%m-%d').year)
                for item in self.result if item['first_air_date']]

    @property
    def confronto(self) -> list:
        """
        un elenco di chiamate API per svolgere le funzioni principali
        Se la data nel file_name è disponibile viene confrontata con i risultati in tmdb per filtrare
        eventuali video con lo stesso nome ma con data differenti.
        Se non disponibile confronta solo il titolo prendendo il primo risulato in cima alla lista
        todo: con quale altro dato in and posso confrontarlo in questo caso ?

        :return: ritorna il titolo con lo stesso anno di uscita e titolo identico
        """
        candidate = self._search('name')
        if self.myguessit.guessit_year:
            return [(title, video_id, year) for title, video_id, year in candidate if
                    year == self.myguessit.guessit_year
                    and utitlity.Manage_titles.clean(title.lower()) ==
                    utitlity.Manage_titles.clean(self.myguessit.guessit_title.lower())]
        else:
            return [(title, video_id, year) for title, video_id, year in candidate
                    if utitlity.Manage_titles.clean(title.lower()) ==
                    utitlity.Manage_titles.clean(self.myguessit.guessit_title.lower())]

    @property
    def adult(self):
        return self._search('adult')

    @property
    def backdrop_path(self):
        return self._search('backdrop_path')

    @property
    def genre_ids(self):
        return self._search('genre_ids')

    @property
    def video_id(self):
        return self._search('id')

    @property
    def original_language(self):
        return self._search('original_language')

    @property
    def overview(self):
        return self._search('overview')

    @property
    def popularity(self):
        return self._search('popularity')

    @property
    def poster_path(self):
        return self._search('poster_path')

    @property
    def vote_average(self):
        return self._search('vote_average')

    @property
    def vote_count(self):
        return self._search('vote_count')

    @property
    def title(self) -> list:
        return self._search('name')

    @property
    def original_title(self):
        return self._search('original_name')

    @property
    def release_date(self):
        return self._search('first_air_date')

    @property
    def translations(self):
        details = self.tv_tmdb.details(self.video_id)
        if getattr(details, 'tagline', False):
            return [r['data']['title'] for r in details['translations']['translations']]

    @property
    def details(self):
        """
        Creo una lista di dizionari dove viene riportato per ogni dizionario titolo tradotto,tagline,videoid
        :return:
        """

        details_dictionary_list = []
        for title, video_id, year in self.video_id:
            details = self.tv_tmdb.details(video_id)
            if getattr(details, 'translations', False):
                details_list = [({"title_key": t['data']['name'], "tagline_value": t['data']['tagline'],
                                  "video_id": video_id})
                                for t in details['translations']['translations'] if t['data']['name']]
                details_dictionary_list.append([details_list, video_id])
        return details_dictionary_list

    def cerca(self):
        if not self.confronto:
            for title_keys, video_id in self.details:
                for title_key in title_keys:
                    if (utitlity.Manage_titles.clean(self.myguessit.guessit_title.lower()) in
                            utitlity.Manage_titles.clean(title_key['title_key'].lower())):
                        if (utitlity.Manage_titles.clean(self.myguessit.guessit_alternative.lower())
                                in utitlity.Manage_titles.clean(title_key['title_key'].lower())):
                            return video_id
        else:
            return self.confronto[0][1]
