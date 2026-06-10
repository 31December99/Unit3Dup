# Opzioni avanzate

Sezione `user_preferences` di `Unit3Dbot.json` (più `console_options` in fondo). Nessuna di queste opzioni è obbligatoria: i default vanno bene per iniziare.

## Screenshot

```json
"NUMBER_OF_SCREENSHOTS": 4,
"COMPRESS_SCSHOT": 3,
"RESIZE_SCSHOT": "False",
"WEBP_ENABLED": "False",
```

| Chiave | Effetto |
|---|---|
| `NUMBER_OF_SCREENSHOTS` | Quanti screenshot estrarre dal video |
| `COMPRESS_SCSHOT` | Livello di compressione delle immagini |
| `RESIZE_SCSHOT` | Ridimensiona gli screenshot prima dell'upload |
| `WEBP_ENABLED` | Aggiunge una webp animata alla descrizione del torrent |

## Duplicati

```json
"DUPLICATE_ON": "true",
"SKIP_DUPLICATE": "false",
"SIZE_TH": 10,
```

| Chiave | Effetto |
|---|---|
| `DUPLICATE_ON` | Attiva il controllo duplicati prima dell'upload (equivale al flag `-dup`) |
| `SKIP_DUPLICATE` | Salta il contenuto se viene trovato un duplicato, senza chiedere |
| `SIZE_TH` | Soglia percentuale: un torrent sul tracker è considerato "stesso contenuto" se la differenza di dimensione rispetto al tuo file è entro questa percentuale |

## Cache

```json
"CACHE_PATH": "no_path",
"CACHE_SCR": "False",
"CACHE_DBONLINE": "False",
```

| Chiave | Effetto |
|---|---|
| `CACHE_PATH` | Cartella della cache (default: `Unit3Dup_config/cache_path`) |
| `CACHE_SCR` | Riusa gli screenshot già estratti |
| `CACHE_DBONLINE` | Mette in cache i risultati di TMDB e delle ricerche online |

## Lingua, anonimato e firma

```json
"PREFERRED_LANG": "all",
"ANON": "False",
"PERSONAL_RELEASE": "False",
"RELEASER_SIGN": "",
"TORRENT_COMMENT": "no_comment",
```

| Chiave | Effetto |
|---|---|
| `PREFERRED_LANG` | Codice lingua preferita (ISO 3166, es. `it`) o `all`: il bot avvisa se l'audio non corrisponde |
| `ANON` | Upload **anonimo**: il tuo username non compare sulla pagina del torrent |
| `PERSONAL_RELEASE` | Marca ogni upload come personal release (equivale al flag `-personal`) |
| `RELEASER_SIGN` | La tua firma da releaser, aggiunta al titolo (max 20 caratteri; vedi [Tag e titoli](../usage/tags.md)) |
| `TORRENT_COMMENT` | Commento inserito nel file `.torrent` |

## Posizione dei tag nel titolo

```json
"TAGS_POSITION_MOVIE": ["title", "year", "part", "version", "resolution", "uhd", "platform", "source", "remux", "multi", "acodec", "channels", "flag", "subtitle", "hdr", "vcodec", "video_encoder"],
"TAGS_POSITION_SERIE": ["title", "season", "version", "resolution", "uhd", "platform", "source", "remux", "multi", "acodec", "channels", "flag", "subtitle", "hdr", "vcodec", "video_encoder"],
```

L'**ordine** con cui i tag compongono il titolo del torrent, per film e serie. Puoi riordinare o togliere voci (minimo 5); i nomi devono restare tra quelli ammessi. Dettagli: [Tag e titoli](../usage/tags.md).

## Watcher

```json
"WATCHER_INTERVAL": 60,
"WATCHER_PATH": "no_path",
"WATCHER_DESTINATION_PATH": "no_path",
```

| Chiave | Effetto |
|---|---|
| `WATCHER_INTERVAL` | Ogni quanti **secondi** il watcher controlla la cartella |
| `WATCHER_PATH` | Cartella monitorata (es. dove scarica il tuo client) |
| `WATCHER_DESTINATION_PATH` | Cartella dove i file vengono spostati e poi caricati |

Come funziona: [Watcher](../usage/watcher.md).

## Percorsi

```json
"TORRENT_ARCHIVE_PATH": "no_path",
```

Cartella dove il bot archivia i `.torrent` generati, organizzati in sottocartelle per tracker (`<archivio>/ITT/...`). Con `no_path` usa il default dentro `Unit3Dup_config`.

## YouTube

```json
"YOUTUBE_FAV_CHANNEL_ID": "UC...",
"YOUTUBE_CHANNEL_ENABLE": "False",
"SKIP_YOUTUBE": "true",
"SKIP_TMDB": "false",
```

| Chiave | Effetto |
|---|---|
| `YOUTUBE_FAV_CHANNEL_ID` | Canale preferito da cui pescare i trailer |
| `YOUTUBE_CHANNEL_ENABLE` | Abilita la ricerca trailer sul canale preferito |
| `SKIP_YOUTUBE` | Salta del tutto la ricerca trailer su YouTube |
| `SKIP_TMDB` | Salta l'interrogazione di TMDB (sconsigliato per i video) |

## FAST_LOAD

```json
"FAST_LOAD": "0",
```

Limita il numero di contenuti processati per ogni esecuzione (valori utili: 1–150; `0` = nessun limite). Comodo per testare uno `-scan` su una cartella enorme senza processarla tutta.

## Colori della console (`console_options`)

```json
"console_options": {
    "NORMAL_COLOR": "blue bold",
    "ERROR_COLOR": "red bold",
    "WELCOME_MESSAGE": "https://itatorrents.xyz",
    "WELCOME_MESSAGE_COLOR": "blue",
    "WELCOME_MESSAGE_BORDER_COLOR": "yellow",
    "PANEL_MESSAGE_COLOR": "blue",
    "PANEL_MESSAGE_BORDER_COLOR": "yellow",
    "QUESTION_MESSAGE_COLOR": "yellow"
}
```

Personalizza testo e colori dell'output. Colori ammessi: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, anche in variante `bold` (es. `"cyan bold"`).
