# Unit3Dup

**Unit3Dup is a Python bot that generates and uploads your torrents to UNIT3D-based trackers.**

Give it a path — a file or a folder — and it does the rest: it analyzes your media, creates the torrent, prepares the tracker page and starts seeding.

## What it does

- Scans folders and subfolders
- Collects metadata and creates the `.torrent` file
- Extracts a series of screenshots straight from the video and uploads them to an image host
- Looks up the matching ID on **TMDB**, **IMDB**, **TVDB**, **IGDB**
- Adds the trailer from TMDB or YouTube
- Generates the title tags: `version`, `resolution`, `uhd`, `platform`, `source`, `remux`, `multi`, `acodec`, `channels`, `flag`, `subtitle`, `vcodec`, `hdr`, `video_encoder`
- Extracts the cover from PDF documents
- Seeds with **qBittorrent**, **Transmission** or **rTorrent**
- Reseeds one or more torrents at a time, even across different OSes

## Quickstart

Three commands cover most use cases:

```bash
unit3dup -u "/home/ITT/upload/movie.mkv"
```

Uploads a **single file**: analysis, screenshots, upload, seeding.

```bash
unit3dup -f "/home/ITT/upload/foldername"
```

Uploads a **folder** as a single torrent (a movie, a full season…). The torrent takes the folder name.

```bash
unit3dup -scan "/home/ITT/upload"
```

Processes **everything** inside the path: every file and every folder, all the way to seeding.

!!! tip "First time?"
    Follow the [First upload step by step](guides/first-upload.md) guide: from installation to your first uploaded torrent.

## How the bot thinks

The flow is always the same:

1. You provide a **path** (file or folder)
2. The bot analyzes the content and creates an **object** for each item
3. Every object has **properties** describing what will be uploaded
4. The properties are sent to the tracker together with the torrent

### Video object

Created for every video file found:

| Property | Description |
|---|---|
| `name` | Torrent name and title shown on the tracker page |
| `tmdb` | ID obtained by querying TheMovieDatabase |
| `tvdb` | ID obtained by querying TheTVDB |
| `imdb` | ID derived from the TVDB result |
| `keywords` | Keywords obtained from the TMDB result |
| `category_id` | Tracker category: Movie or TV show |
| `resolution_id` | Resolution as recognized by the tracker |
| `sd` | Whether the video is SD or at least HD |
| `anonymous` | If set, hides your username |
| `mediainfo` | MediaInfo output with the technical details of the video |
| `description` | Screenshots, trailer and personal description |
| `type_id` | Video source (Disc, Remux, Encode, WEB-DL…) |
| `season_number` | Season number |
| `episode_number` | Episode number, `0` for a torrent pack |
| `personal_release` | Marks the torrent as a personal release |

### Document object

It has fewer properties than the video object: `name`, `tmdb`, `category_id`, `anonymous`, `description`, `type_id`, `resolution_id`, `personal_release`. The `tmdb` and `resolution_id` fields are set to neutral values because the tracker requires them. See the [PDF documents](guides/documents.md) guide.

### Game object

Like Documents, plus the `igdb` property: the game ID on the IGDB database. It requires an IGDB account — see the [Games](guides/games.md) guide.

## Supported trackers

| Tracker | Site |
|---|---|
| `ITT` | [itatorrents.xyz](https://itatorrents.xyz) |
| `PTT` | [polishtorrent.top](https://polishtorrent.top) |
| `AST` | [arabicsource.net](https://arabicsource.net) |
| `SIS` | — |

## Community

Questions, reports, requests: [ITT Discord server](https://discord.gg/8RpwN2Khcz).
