# Unit3Dup

**Unit3Dup è un bot scritto in Python che genera e carica i tuoi torrent sui tracker basati su UNIT3D.**

Gli dai un percorso — un file o una cartella — e lui fa il resto: analizza i media, crea il torrent, prepara la pagina del tracker e mette tutto in seeding.

## Cosa fa

- Scansiona cartelle e sottocartelle
- Raccoglie i metadati e crea il file `.torrent`
- Estrae una serie di screenshot direttamente dal video e li carica su un image host
- Cerca l'ID corrispondente su **TMDB**, **IMDB**, **TVDB**, **IGDB**
- Aggiunge il trailer da TMDB o YouTube
- Genera i tag del titolo: `version`, `resolution`, `uhd`, `platform`, `source`, `remux`, `multi`, `acodec`, `channels`, `flag`, `subtitle`, `vcodec`, `hdr`, `video_encoder`
- Estrae la cover dai documenti PDF
- Mette in seeding su **qBittorrent**, **Transmission** o **rTorrent**
- Fa il reseed di uno o più torrent alla volta, anche tra OS diversi

## Quickstart

Tre comandi coprono la maggior parte dei casi:

```bash
unit3dup -u "/home/ITT/upload/film.mkv"
```

Carica un **singolo file**: analisi, screenshot, upload, seeding.

```bash
unit3dup -f "/home/ITT/upload/nomecartella"
```

Carica una **cartella** come unico torrent (un film, una stagione completa…). Il torrent prende il nome della cartella.

```bash
unit3dup -scan "/home/ITT/upload"
```

Processa **tutto il contenuto** del percorso: ogni file e ogni cartella, fino al seeding.

!!! tip "Prima volta?"
    Segui la guida [Primo upload passo-passo](guides/first-upload.md): dall'installazione al primo torrent caricato.

## Come ragiona il bot

Il flusso è sempre lo stesso:

1. Tu fornisci un **percorso** (file o cartella)
2. Il bot analizza il contenuto e crea per ogni elemento un **oggetto**
3. Ogni oggetto ha delle **proprietà** che descrivono cosa verrà caricato
4. Le proprietà vengono trasmesse al tracker insieme al torrent

### Oggetto Video

Creato per ogni file video incontrato:

| Proprietà | Descrizione |
|---|---|
| `name` | Nome del torrent e titolo visualizzato sulla pagina del tracker |
| `tmdb` | ID ottenuto interrogando TheMovieDatabase |
| `tvdb` | ID ottenuto interrogando TheTVDB |
| `imdb` | ID ricavato dal risultato di TVDB |
| `keywords` | Keywords ottenute dal risultato di TMDB |
| `category_id` | Categoria del tracker: Movie o Serie |
| `resolution_id` | Risoluzione riconosciuta dal tracker |
| `sd` | Indica se il video è SD oppure almeno HD |
| `anonymous` | Se attivo, nasconde il tuo username |
| `mediainfo` | Output di MediaInfo con i dati tecnici del video |
| `description` | Screenshot, trailer e descrizione personale |
| `type_id` | Sorgente del video (Disc, Remux, Encode, WEB-DL…) |
| `season_number` | Numero di stagione |
| `episode_number` | Numero di episodio, `0` se è un torrent pack |
| `personal_release` | Marca il torrent come personal release |

### Oggetto Documenti

Ha meno proprietà del video: `name`, `tmdb`, `category_id`, `anonymous`, `description`, `type_id`, `resolution_id`, `personal_release`. I campi `tmdb` e `resolution_id` sono impostati a valori neutri perché il tracker li considera obbligatori. Vedi la guida [Documenti PDF](guides/documents.md).

### Oggetto Game

Come Documenti, con in più la proprietà `igdb`: l'ID del gioco sul database IGDB. Richiede un account IGDB — vedi la guida [Giochi](guides/games.md).

## Tracker supportati

| Tracker | Sito |
|---|---|
| `ITT` | [itatorrents.xyz](https://itatorrents.xyz) |
| `PTT` | [polishtorrent.top](https://polishtorrent.top) |
| `AST` | [arabicsource.net](https://arabicsource.net) |
| `SIS` | — |

## Community

Domande, segnalazioni, richieste: [server Discord di ITT](https://discord.gg/8RpwN2Khcz).
