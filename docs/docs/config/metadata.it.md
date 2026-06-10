# Metadata

Sezione `tracker_config` di `Unit3Dbot.json` — le chiavi dei servizi esterni che il bot interroga per identificare i tuoi contenuti.

## TMDB_APIKEY

```json
"TMDB_APIKEY": "la_tua_chiave",
```

**TheMovieDatabase** è il servizio principale: il bot lo interroga per ottenere l'**ID del titolo** (film o serie) da trasmettere al tracker, le keywords, e il trailer.

Chiave gratuita: registrati su [themoviedb.org](https://www.themoviedb.org/), poi *Impostazioni → API*.

## TVDB_APIKEY

```json
"TVDB_APIKEY": "la_tua_chiave",
```

**TheTVDB** viene interrogato per le serie TV; dal suo risultato il bot ricava anche l'**ID IMDB**. Chiave su [thetvdb.com](https://thetvdb.com/) → API.

## YOUTUBE_KEY

```json
"YOUTUBE_KEY": "la_tua_chiave",
```

Usata per cercare il **trailer** su YouTube quando TMDB non lo fornisce. Chiave API da [Google Cloud Console](https://console.cloud.google.com/) (YouTube Data API v3).

Vedi anche `SKIP_YOUTUBE`, `YOUTUBE_FAV_CHANNEL_ID` e `YOUTUBE_CHANNEL_ENABLE` nelle [Opzioni avanzate](options.md).

## IGDB_CLIENT_ID e IGDB_ID_SECRET

```json
"IGDB_CLIENT_ID": "il_tuo_client_id",
"IGDB_ID_SECRET": "il_tuo_secret",
```

**IGDB** identifica i **giochi**. Le credenziali si ottengono dalla [console sviluppatori di Twitch](https://dev.twitch.tv/console) (IGDB è di Twitch).

!!! warning "Senza credenziali IGDB i giochi vengono saltati"
    Se `IGDB_CLIENT_ID` resta `no_key`, il bot salta l'upload dei giochi con il messaggio `Skipping game upload, no IGDB credentials provided`. Film, serie e documenti non sono toccati.

Guida completa: [Giochi](../guides/games.md).
