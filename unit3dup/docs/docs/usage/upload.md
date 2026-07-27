# Basic upload

The three core flags: `-u`, `-f`, `-scan`. All of them run the full pipeline — analysis, screenshots, metadata lookup, `.torrent` creation, tracker upload, client seeding.

## `-u` — a single file

```bash
unit3dup -u "/home/ITT/upload/movie.mkv"
```

Uploads **one file**. The bot analyzes it, derives title and tags from the name, creates the torrent.

## `-f` — a folder

```bash
unit3dup -f "/home/ITT/upload/foldername"
```

Creates **a single torrent with the folder contents**, named after the folder. It can hold a movie or a TV show: the bot doesn't care.

Use it for: full seasons, multi-part movies, content with companion files.

## `-scan` — everything inside a path

```bash
unit3dup -scan "/home/ITT/upload"
```

It's `-u` and `-f` combined: it analyzes **every file and every folder** inside the path (recursively) and processes everything, one torrent per item found.

!!! tip "Too much content?"
    On very large folders you can cap the number of processed items with `FAST_LOAD` in the [Advanced options](../config/options.md).

## Modifiers

They combine with `-u`, `-f` and `-scan`:

| Flag | Effect |
|---|---|
| `-noup` | Creates the `.torrent` only (in the [archive](../config/options.md#paths)), **no upload** and no seeding |
| `-noseed` | Upload to the tracker **without seeding**: the torrent is not handed to the client |
| `-dup` | Checks the tracker for [duplicates](../config/options.md#duplicates) before uploading |
| `-personal` | Marks the upload as a **personal release** |
| `-force <category>` | Forces the category: `movie`, `tv`, `game`, `edicola` (without argument: `movie`) |
| `-notitle "<title>"` | Uses this title for the TMDB search instead of the one derived from the file name |
| `-b` | Rebuilds title and tags ([Tags and titles](tags.md)) |
| `-tracker <NAME>` / `-mt` | Destination tracker ([Multi-tracker](multitracker.md)) |
| `-reseed` | Reseed mode ([Reseed](reseed.md)) |

## Full example

```bash
unit3dup -mt -b -u "/home/parzival/TEST/scan/007 - Live and Let Die (1973).mkv"
```

Analyzes the file, rebuilds title and tags, uploads it to **all** configured trackers and starts seeding.

!!! note "What you see on screen"
    The bot prints a table of the files being processed, then for each item: TMDB lookup, screenshot extraction, image upload, torrent creation, tracker response, hand-off to the client. The [First upload step by step](../guides/first-upload.md) guide describes every stage.
