# Tracker search

Besides uploading, the bot queries the tracker from the terminal: searches, details, filters. Every command runs against the **default tracker** (the first in `MULTI_TRACKER`) or the one given with `-tracker <NAME>`.

## Basic searches

| Command | What it does |
|---|---|
| `-sch "<text>"` | Searches torrents by title |
| `-i "<text>"` | Like `-sch` but shows the **detailed information** of every result |
| `-dmp` | **Full dump** of all the tracker titles (saved locally) |
| `-up "<uploader>"` | Torrents by a given uploader |
| `-d "<text>"` | Searches inside the **descriptions** |
| `-bd "<text>"` | Shows the **BDInfo** of the matching torrents |
| `-m "<text>"` | Shows the **MediaInfo** of the matching torrents |
| `-db` | Added to a search, **saves the results** to the local database |

```bash
unit3dup -sch "movie title"
unit3dup -tracker ptt -sch "movie title"
unit3dup -up "UploaderName" -db
```

## Filters

| Filter | Meaning |
|---|---|
| `-st <year>` / `-en <year>` | From year / up to year |
| `-type <type>` | Content type |
| `-res <resolution>` | Resolution |
| `-file "<name>"` | File name |
| `-se <n>` / `-ep <n>` | Season / episode |
| `-tmdb <id>` `-imdb <id>` `-tvdb <id>` `-mal <id>` | By external database IDs |
| `-playid <id>` / `-coll <id>` | Playlist / collection |
| `-free <value>` | Freeleech percentage |
| `-al` / `-dd` / `-dy` | Status: alive / dead / dying |

Useful combo — one TMDB title at a specific resolution:

```bash
unit3dup -tmdb 603 -res 1080p
```

## Special views

Lists by torrent attribute:

| Flag | Shows |
|---|---|
| `-du` | DoubleUp |
| `-fe` | Featured |
| `-re` | Refundable |
| `-str` | Stream-friendly |
| `-sd` | Standard definition |
| `-hs` | Highspeed |
| `-int` | Internal |
| `-pr` | Personal release |

```bash
unit3dup -fe
```

The full table of every flag: [All commands](../reference/commands.md).
