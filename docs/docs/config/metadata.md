# Metadata

`tracker_config` section of `Unit3Dbot.json` — the keys for the external services the bot queries to identify your content.

## TMDB_APIKEY

```json
"TMDB_APIKEY": "your_key",
```

**TheMovieDatabase** is the main service: the bot queries it to get the **title ID** (movie or TV show) to send to the tracker, plus keywords and the trailer.

Free key: sign up at [themoviedb.org](https://www.themoviedb.org/), then *Settings → API*.

## TVDB_APIKEY

```json
"TVDB_APIKEY": "your_key",
```

**TheTVDB** is queried for TV shows; the bot also derives the **IMDB ID** from its result. Get a key at [thetvdb.com](https://thetvdb.com/) → API.

## YOUTUBE_KEY

```json
"YOUTUBE_KEY": "your_key",
```

Used to search the **trailer** on YouTube when TMDB doesn't provide one. API key from [Google Cloud Console](https://console.cloud.google.com/) (YouTube Data API v3).

See also `SKIP_YOUTUBE`, `YOUTUBE_FAV_CHANNEL_ID` and `YOUTUBE_CHANNEL_ENABLE` in [Advanced options](options.md).

## IGDB_CLIENT_ID and IGDB_ID_SECRET

```json
"IGDB_CLIENT_ID": "your_client_id",
"IGDB_ID_SECRET": "your_secret",
```

**IGDB** identifies **games**. Credentials come from the [Twitch developer console](https://dev.twitch.tv/console) (IGDB belongs to Twitch).

!!! warning "Without IGDB credentials, games are skipped"
    If `IGDB_CLIENT_ID` stays `no_key`, the bot skips game uploads with the message `Skipping game upload, no IGDB credentials provided`. Movies, TV shows and documents are not affected.

Full guide: [Games](../guides/games.md).
