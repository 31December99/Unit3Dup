# Config completa

Ogni chiave di `Unit3Dbot.json`, sezione per sezione. "Default" è il valore nel file generato al primo avvio; i segnaposto `no_key` / `no_pass` / `no_path` significano "non configurato".

## `tracker_config`

| Chiave | Tipo | Default | Obbligatoria | Descrizione |
|---|---|---|---|---|
| `ITT_URL` | stringa | `https://itatorrents.xyz` | per usare ITT | URL del tracker ITT |
| `ITT_APIKEY` | stringa | `no_key` | per usare ITT | API key del tuo profilo ITT |
| `ITT_PID` | stringa | `no_key` | se `itt` è in `MULTI_TRACKER` | Passkey ITT |
| `SIS_URL` | stringa | `https://no_tracker.xyz` | per usare SIS | URL del tracker SIS |
| `SIS_APIKEY` | stringa | `no_key` | per usare SIS | API key SIS |
| `SIS_PID` | stringa | `no_key` | se `sis` è in `MULTI_TRACKER` | Passkey SIS |
| `PTT_URL` | stringa | `https://polishtorrent.top` | per usare PTT | URL del tracker PTT |
| `PTT_APIKEY` | stringa | `no_key` | per usare PTT | API key PTT |
| `PTT_PID` | stringa | `no_key` | se `ptt` è in `MULTI_TRACKER` | Passkey PTT |
| `AST_URL` | stringa | `https://arabicsource.net` | per usare AST | URL del tracker AST |
| `AST_APIKEY` | stringa | `no_key` | per usare AST | API key AST |
| `AST_PID` | stringa | `no_key` | se `ast` è in `MULTI_TRACKER` | Passkey AST |
| `MULTI_TRACKER` | lista | `["itt","sis","ptt","ast"]` | sì (non vuota) | Tracker attivi; il primo è il default. Niente duplicati |
| `TMDB_APIKEY` | stringa | `no_key` | per i video | Chiave TheMovieDB |
| `TVDB_APIKEY` | stringa | `no_key` | consigliata per le serie | Chiave TheTVDB |
| `IMGBB_KEY` | stringa | `no_key` | almeno un host | Chiave ImgBB |
| `FREE_IMAGE_KEY` | stringa | `no_key` | almeno un host | Chiave FreeImage |
| `LENSDUMP_KEY` | stringa | `no_key` | almeno un host | Chiave LensDump |
| `PTSCREENS_KEY` | stringa | `no_key` | almeno un host | Chiave PtScreens |
| `IMGFI_KEY` | stringa | `no_key` | almeno un host | Chiave ImgFI |
| `PASSIMA_KEY` | stringa | `no_key` | almeno un host | Chiave PassIMA |
| `IMARIDE_KEY` | stringa | `no_key` | almeno un host | Chiave ImaRide |
| `YOUTUBE_KEY` | stringa | `no_key` | no | Chiave YouTube Data API (trailer) |
| `IGDB_CLIENT_ID` | stringa | `no_key` | per i giochi | Client ID IGDB/Twitch |
| `IGDB_ID_SECRET` | stringa | `no_key` | per i giochi | Client Secret IGDB/Twitch |

## `torrent_client_config`

| Chiave | Tipo | Default | Obbligatoria | Descrizione |
|---|---|---|---|---|
| `QBIT_USER` | stringa | `admin` | se usi qBittorrent | Username WebUI |
| `QBIT_PASS` | stringa | `no_pass` | se usi qBittorrent | Password WebUI |
| `QBIT_HOST` | stringa | `127.0.0.1` | se usi qBittorrent | Host del client |
| `QBIT_PORT` | numero | `8080` | se usi qBittorrent | Porta WebUI |
| `SHARED_QBIT_PATH` | stringa | `no_path` | no | Percorso visto dal client se gira altrove |
| `TRASM_USER` | stringa | `admin` | se usi Transmission | Username |
| `TRASM_PASS` | stringa | `no_pass` | se usi Transmission | Password |
| `TRASM_HOST` | stringa | `127.0.0.1` | se usi Transmission | Host |
| `TRASM_PORT` | numero | `9091` | se usi Transmission | Porta |
| `SHARED_TRASM_PATH` | stringa | `no_path` | no | Percorso visto dal client se gira altrove |
| `RTORR_USER` | stringa | `admin` | se usi rTorrent | Username |
| `RTORR_PASS` | stringa | `no_pass` | se usi rTorrent | Password |
| `RTORR_HOST` | stringa | `127.0.0.1` | se usi rTorrent | Host |
| `RTORR_PORT` | numero | `9091` | se usi rTorrent | Porta |
| `SHARED_RTORR_PATH` | stringa | `no_path` | no | Percorso visto dal client se gira altrove |
| `TORRENT_CLIENT` | stringa | `qbittorrent` | per upload con seeding | `qbittorrent`, `transmission` o `rtorrent` |
| `TAG` | stringa | `ADDED TORRENTS` | no | Etichetta applicata ai torrent nel client |

## `user_preferences`

| Chiave | Tipo | Default | Descrizione |
|---|---|---|---|
| `PTSCREENS_PRIORITY` | numero | `0` | Priorità host immagini (0 = primo) |
| `LENSDUMP_PRIORITY` | numero | `1` | Priorità LensDump |
| `FREE_IMAGE_PRIORITY` | numero | `2` | Priorità FreeImage |
| `IMGBB_PRIORITY` | numero | `3` | Priorità ImgBB |
| `IMGFI_PRIORITY` | numero | `4` | Priorità ImgFI |
| `PASSIMA_PRIORITY` | numero | `5` | Priorità PassIMA |
| `IMARIDE_PRIORITY` | numero | `6` | Priorità ImaRide |
| `NUMBER_OF_SCREENSHOTS` | numero | `4` | Screenshot estratti dal video (2–10) |
| `TAGS_POSITION_MOVIE` | lista | vedi [Opzioni](../config/options.md#posizione-dei-tag-nel-titolo) | Ordine dei tag nei titoli dei film (5–17 voci) |
| `TAGS_POSITION_SERIE` | lista | vedi [Opzioni](../config/options.md#posizione-dei-tag-nel-titolo) | Ordine dei tag nei titoli delle serie |
| `YOUTUBE_FAV_CHANNEL_ID` | stringa | canale ITT | Canale YouTube preferito per i trailer |
| `YOUTUBE_CHANNEL_ENABLE` | booleano | `False` | Abilita la ricerca sul canale preferito |
| `DUPLICATE_ON` | booleano | `true` | Controllo duplicati a ogni upload |
| `SKIP_DUPLICATE` | booleano | `false` | Salta i contenuti duplicati senza chiedere |
| `SKIP_TMDB` | booleano | `false` | Non interrogare TMDB |
| `SKIP_YOUTUBE` | booleano | `true` | Non cercare trailer su YouTube |
| `SIZE_TH` | numero | `10` | Soglia % di differenza dimensione per il match duplicati |
| `WATCHER_INTERVAL` | numero | `60` | Secondi tra i controlli del watcher |
| `WATCHER_PATH` | stringa | `no_path` | Cartella monitorata dal watcher |
| `WATCHER_DESTINATION_PATH` | stringa | `no_path` | Destinazione dei file del watcher |
| `TORRENT_ARCHIVE_PATH` | stringa | `no_path` | Archivio dei `.torrent` generati |
| `CACHE_PATH` | stringa | `no_path` | Cartella cache |
| `COMPRESS_SCSHOT` | numero | `3` | Compressione screenshot |
| `RESIZE_SCSHOT` | booleano | `False` | Ridimensiona gli screenshot |
| `TORRENT_COMMENT` | stringa | `no_comment` | Commento nel file `.torrent` |
| `PREFERRED_LANG` | stringa | `all` | Lingua preferita (ISO 3166) o `all` |
| `ANON` | booleano | `False` | Upload anonimo |
| `WEBP_ENABLED` | booleano | `False` | Webp animata nella descrizione |
| `CACHE_SCR` | booleano | `False` | Cache degli screenshot |
| `CACHE_DBONLINE` | booleano | `False` | Cache delle ricerche online |
| `PERSONAL_RELEASE` | booleano | `False` | Personal release su ogni upload |
| `FAST_LOAD` | numero | `0` | Limita i contenuti processati (1–150; 0 = tutti) |
| `RELEASER_SIGN` | stringa | vuota | Firma releaser (max 20 caratteri) |

## `options`

| Chiave | Tipo | Default | Descrizione |
|---|---|---|---|
| `FTPX_USER` | stringa | `user` | Username FTP |
| `FTPX_PASS` | stringa | `pass` | Password FTP |
| `FTPX_IP` | stringa | `127.0.0.1` | IP del server FTP |
| `FTPX_PORT` | numero | `2121` | Porta FTP |
| `FTPX_LOCAL_PATH` | stringa | `.` | Cartella locale di download |
| `FTPX_ROOT` | stringa | `.` | Cartella remota di partenza |
| `FTPX_KEEP_ALIVE` | booleano | `False` | Mantiene viva la connessione |

## `console_options`

| Chiave | Tipo | Default | Descrizione |
|---|---|---|---|
| `NORMAL_COLOR` | stringa | `blue bold` | Colore messaggi normali |
| `ERROR_COLOR` | stringa | `red bold` | Colore errori |
| `WELCOME_MESSAGE` | stringa | `https://itatorrents.xyz` | Testo del banner di benvenuto |
| `WELCOME_MESSAGE_COLOR` | stringa | `blue` | Colore del banner |
| `WELCOME_MESSAGE_BORDER_COLOR` | stringa | `yellow` | Bordo del banner |
| `PANEL_MESSAGE_COLOR` | stringa | `blue` | Colore dei pannelli |
| `PANEL_MESSAGE_BORDER_COLOR` | stringa | `yellow` | Bordo dei pannelli |
| `QUESTION_MESSAGE_COLOR` | stringa | `yellow` | Colore delle domande |

Colori ammessi: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` (+ ` bold`).

I valori booleani accettano `true`/`false`, `1`/`0`, `yes`/`no` (come stringhe o nativi).
