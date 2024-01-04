# -*- coding: utf-8 -*-
from unidecode import unidecode
from utitlity import Manage_titles
from decouple import config
from tmdbv3api import TMDb, Movie, TV
from results import Results
import tmdbv3api.exceptions
import guessit
from thefuzz import fuzz

TMDB_APIKEY = config('TMDB_APIKEY')


class Myguessit:

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


class MyTmdb:

    def __init__(self, table: str, year='', videoid=''):
        self.table = table
        self.ext_title = None
        self.year = year
        self.videoid = videoid
        self.tmdb = None
        self._tmdb = TMDb()
        self._tmdb.language = 'it-EN'  # todo: problema con titoli per metà ita o en or it-en ? commuta da solo ?
        self._tmdb.api_key = TMDB_APIKEY
        self.__mv_tmdb = Movie()
        self.__tv_tmdb = TV()
        self.__result = None
        self.__page = []

        if self.table == 'Serie':
            self.tmdb = self.__tv_tmdb

        if self.table == 'Movie':
            self.tmdb = self.__mv_tmdb

    def search(self, ext_title: str):
        self.ext_title = ext_title
        self.__requests()
        result = self.__search_titles()
        if not result:
            result = self.__search_alternative()
            if not result:
                result = self.__search_translations()
        if result:
            result.keywords = self.keywords(result.video_id)
        return result

    def __requests(self):
        self.ext_title = self.ext_title  # Manage_titles.prefil(self.ext_title)
        self.__result = self.tmdb.search(self.ext_title)
        print(f"\n[TMDB Search]..........  {self.ext_title}")
        print(f"[TMDB obj].............  {self.tmdb}")
        print(f"[TMDB total-results]...  {self.__result['total_results']}")
        print(f"[TMDB total-pages].....  {self.__result['total_pages']}")
        if self.__result['total_results'] > 0:
            for result in self.__result:
                results = Results()
                try:
                    if isinstance(self.tmdb, TV):
                        results.title = result['name']
                        results.original_title = result['original_name']
                        results.date = result['first_air_date']

                    if isinstance(self.tmdb, Movie):
                        results.title = result['title']
                        results.original_title = result['original_title']
                        results.date = getattr(result, 'release_date', '')
                    # ALL
                    results.genre_ids = getattr(result, 'genre_ids', '')
                    results.video_id = result['id']
                    results.poster_path = result['poster_path']
                    results.backdrop_path = result['backdrop_path']
                    results.overview = result['overview']
                    results.popularity = getattr(result, 'popularity', '')
                    details = self.tmdb.details(result['id'])

                    if 'translations' in details:
                        for iso in details['translations']['translations']:
                            results.translations.append(iso)
                        results.alternative.append(self.tmdb.alternative_titles(result['id']))
                except tmdbv3api.exceptions.TMDbException as e:
                    # print(f">>>>>>>> ** TMDB ** <<<<<<<<<{e} - tmdb details non disponibile")
                    results.translations = []
                    results.alternative = []
                self.__page.append(results)

    def details(self, video_id: str):
        return self.tmdb.details(video_id)

    def __search_alternative(self):
        field = 'titles' if isinstance(self.tmdb, Movie) else 'results'
        for index, page in enumerate(self.__page):
            # print(f".:: ALTERNATIVE n°{index} ::.")
            for iso in page.alternative:
                results = iso[field]
                ext_title = Manage_titles.clean(unidecode(self.ext_title))
                if len(iso[field]) > 0:
                    for result in results:
                        title = Manage_titles.clean(unidecode(result['title']))
                        # print(f"EXT_T: {ext_title} = ALTERNATIVE TITLE: {title}")
                        if ext_title == title:
                            return page
                        else:
                            ratio = fuzz.ratio(ext_title, title)
                            # print(f"EXT_T: {ext_title} VS ALTERNATIVE TITLE: {title} RATIO: {ratio}\n")
                            if ratio > 95:
                                return page

    def __search_titles(self):
        """
         Confronto il titolo di ogni risultato nella pagina con il titolo in input
        :return:
        """
        for index, page in enumerate(self.__page):
            original_title = Manage_titles.clean(Manage_titles.accented_remove(page.original_title))
            title = Manage_titles.clean(Manage_titles.accented_remove(page.title))
            ext_title = Manage_titles.clean(Manage_titles.accented_remove(self.ext_title))
            # print(f".:: RESULT n°{index} ::.")
            if original_title:
                # print(f"EXT_T: {ext_title} = ORIGINAL TITLE: {original_title}")
                if ext_title == original_title:
                    return page
                else:
                    ratio = fuzz.ratio(ext_title, original_title)
                    # print(f"EXT_T: {ext_title} VS ORIGINAL TITLE: {original_title} RATIO: {ratio}\n")
                    if ratio > 95:
                        return page
            if title:
                # print(f"EXT_T: {ext_title} = TITLE: {title}")
                if ext_title == title:
                    return page
                else:
                    ratio = fuzz.ratio(ext_title, title)
                    # print(f"EXT_T: {ext_title} VS TITLE:{title} RATIO: {ratio}\n")
                    if ratio > 95:
                        return page

    def __search_translations(self):
        """
         Confronto le traduzioni di ogni risultato nella pagina con il titolo in input
        :return:
        """
        for index, page in enumerate(self.__page):
            for translation in page.translations:
                if 'title' in translation['data']:
                    name = translation['data'].get('title', '')
                else:
                    name = translation['data'].get('name', '')
                name = Manage_titles.clean(unidecode(name))
                tagline = Manage_titles.clean(Manage_titles.accented_remove(translation['data']['tagline']))
                ext_title = Manage_titles.clean(unidecode(self.ext_title))
                if name:
                    if ext_title == name:
                        # todo aggiungere anche confronto con Year ?
                        return page
                    else:
                        ratio = fuzz.ratio(ext_title, name)
                        # print(f"EXT_T: {ext_title} VS TRANSLATION NAME {name} RATIO {ratio}\n")
                        if ratio > 95:
                            return page
                if tagline:
                    if ext_title == tagline:
                        # print(f"EXT_T: {ext_title} = TAGLINE {tagline} ?")
                        if self.ext_title in tagline:
                            # todo aggiungere anche confronto con Year ?
                            return page
                        else:
                            ratio = fuzz.ratio(ext_title, tagline)
                            # print(f"EXT_T: {ext_title} = TAGLINE {tagline} RATIO {ratio}\n")
                            if ratio > 95:
                                return page

    def keywords(self, video_id: int) -> str:
        details = self.tmdb.details(video_id)
        if "keywords" in details:
            keywords = details.keywords
            if keywords['keywords']:
                keywords = ','.join([key['name'] for key in keywords['keywords']])
                return keywords
