# All commands

Synopsis:

```text
unit3dup [options]
```

Upload flags combine with each other (e.g. `-mt -b -u "<file>"`); search flags combine with the filters. Every flag also has a long form (`-u` / `--upload`).

## Configuration

| Flag | Argument | Description |
|---|---|---|
| `-check` | — | Checks the configuration files and the environment |

## Upload

| Flag | Argument | Description |
|---|---|---|
| `-u`, `--upload` | file path | Uploads a [single file](../usage/upload.md#-u-a-single-file) |
| `-f`, `--folder` | folder path | Uploads a [folder](../usage/upload.md#-f-a-folder) as a single torrent |
| `-scan` | path | Processes [everything](../usage/upload.md#-scan-everything-inside-a-path) inside the path |
| `-b`, `--buildtags` | — | [Rebuilds title and tags](../usage/tags.md#-b-rebuild-the-title) from the media analysis |
| `-reseed` | — | [Reseed](../usage/reseed.md): downloads from the tracker the torrents of your local content |
| `-watcher` | — | Starts the [watcher](../usage/watcher.md) (monitored folder) |
| `-notitle` | "title" | [Manual title](../usage/tags.md#manual-title) for the TMDB search |
| `-tracker` | tracker name | [Destination tracker](../usage/multitracker.md#-tracker-one-specific-tracker) (default: the first in `MULTI_TRACKER`) |
| `-mt` | — | Upload to [all configured trackers](../usage/multitracker.md#-mt-all-trackers) |
| `-force` | category | Forces the category: `movie`, `tv`, `game`, `edicola` (no argument: `movie`) |
| `-noseed` | — | Upload without handing the torrent to the client (no seeding) |
| `-noup` | — | Creates the `.torrent` in the archive only, no upload |
| `-dup`, `--duplicate` | — | Checks the tracker for duplicates before uploading |
| `-personal` | — | Marks as personal release |
| `-ftp` | — | [Interactive FTP browser](../usage/ftp.md): download from the remote server and upload |

## Search

| Flag | Argument | Description |
|---|---|---|
| `-sch`, `--search` | "text" | [Searches](../usage/search.md) torrents by title |
| `-i`, `--info` | "text" | Like `-sch` with detailed information |
| `-dmp`, `--dump` | — | Full dump of the tracker titles (saved locally) |
| `-db`, `--dbsave` | — | Saves the search results to the local database |
| `-up`, `--uploader` | "name" | Torrents by uploader |
| `-d`, `--description` | "text" | Searches inside descriptions |
| `-bd`, `--bdinfo` | "text" | Shows the BDInfo of the results |
| `-m`, `--mediainfo` | "text" | Shows the MediaInfo of the results |

## Filters

| Flag | Argument | Description |
|---|---|---|
| `-st`, `--startyear` | year | From this year on |
| `-en`, `--endyear` | year | Up to this year |
| `-type` | type | Content type |
| `-res`, `--resolution` | resolution | Filter by resolution |
| `-file`, `--filename` | "name" | Filter by file name |
| `-se`, `--season` | number | Season |
| `-ep`, `--episode` | number | Episode |
| `-tmdb` | ID | By TMDB ID (with `-res`: title+resolution combo) |
| `-imdb` | ID | By IMDB ID |
| `-tvdb` | ID | By TVDB ID |
| `-mal` | ID | By MyAnimeList ID |
| `-playid` | ID | By playlist |
| `-coll` | ID | By collection |
| `-free` | percentage | By freeleech percentage |
| `-al`, `--alive` | — | Alive torrents only |
| `-dd`, `--dead` | — | Dead torrents only |
| `-dy`, `--dying` | — | Dying torrents only |

## Special views

| Flag | Description |
|---|---|
| `-du`, `--doubleup` | DoubleUp torrents |
| `-fe`, `--featured` | Featured torrents |
| `-re`, `--refundable` | Refundable torrents |
| `-str`, `--stream` | Stream-friendly torrents |
| `-sd`, `--standard` | SD torrents |
| `-hs`, `--highspeed` | Highspeed torrents |
| `-int`, `--internal` | Internal releases |
| `-pr`, `--prelease` | Personal releases |
