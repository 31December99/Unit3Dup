# Advanced options

`user_preferences` section of `Unit3Dbot.json` (plus `console_options` at the bottom). None of these options is required: the defaults are fine to start with.

## Screenshots

```json
"NUMBER_OF_SCREENSHOTS": 4,
"COMPRESS_SCSHOT": 3,
"RESIZE_SCSHOT": "False",
"WEBP_ENABLED": "False",
```

| Key | Effect |
|---|---|
| `NUMBER_OF_SCREENSHOTS` | How many screenshots to extract from the video |
| `COMPRESS_SCSHOT` | Image compression level |
| `RESIZE_SCSHOT` | Resize screenshots before uploading |
| `WEBP_ENABLED` | Adds an animated webp to the torrent description |

## Duplicates

```json
"DUPLICATE_ON": "true",
"SKIP_DUPLICATE": "false",
"SIZE_TH": 10,
```

| Key | Effect |
|---|---|
| `DUPLICATE_ON` | Enables the duplicate check before every upload (same as the `-dup` flag) |
| `SKIP_DUPLICATE` | Skips the content when a duplicate is found, without asking |
| `SIZE_TH` | Percentage threshold: a torrent on the tracker counts as "same content" if its size differs from your file within this percentage |

## Cache

```json
"CACHE_PATH": "no_path",
"CACHE_SCR": "False",
"CACHE_DBONLINE": "False",
```

| Key | Effect |
|---|---|
| `CACHE_PATH` | Cache folder (default: `Unit3Dup_config/cache_path`) |
| `CACHE_SCR` | Reuses screenshots already extracted |
| `CACHE_DBONLINE` | Caches TMDB results and online searches |

## Language, anonymity and signature

```json
"PREFERRED_LANG": "all",
"ANON": "False",
"PERSONAL_RELEASE": "False",
"RELEASER_SIGN": "",
"TORRENT_COMMENT": "no_comment",
```

| Key | Effect |
|---|---|
| `PREFERRED_LANG` | Preferred language code (ISO 3166, e.g. `it`) or `all`: the bot warns when the audio doesn't match |
| `ANON` | **Anonymous** upload: your username doesn't appear on the torrent page |
| `PERSONAL_RELEASE` | Marks every upload as a personal release (same as the `-personal` flag) |
| `RELEASER_SIGN` | Your releaser signature, appended to the title (max 20 characters; see [Tags and titles](../usage/tags.md)) |
| `TORRENT_COMMENT` | Comment embedded in the `.torrent` file |

## Tag order in the title

```json
"TAGS_POSITION_MOVIE": ["title", "year", "part", "version", "resolution", "uhd", "platform", "source", "remux", "multi", "acodec", "channels", "flag", "subtitle", "hdr", "vcodec", "video_encoder"],
"TAGS_POSITION_SERIE": ["title", "season", "version", "resolution", "uhd", "platform", "source", "remux", "multi", "acodec", "channels", "flag", "subtitle", "hdr", "vcodec", "video_encoder"],
```

The **order** in which tags build the torrent title, for movies and TV shows. You can reorder or remove entries (minimum 5); names must stay within the allowed set. Details: [Tags and titles](../usage/tags.md).

## Watcher

```json
"WATCHER_INTERVAL": 60,
"WATCHER_PATH": "no_path",
"WATCHER_DESTINATION_PATH": "no_path",
```

| Key | Effect |
|---|---|
| `WATCHER_INTERVAL` | How many **seconds** between watcher checks |
| `WATCHER_PATH` | Watched folder (e.g. where your client downloads) |
| `WATCHER_DESTINATION_PATH` | Folder where files are moved and then uploaded |

How it works: [Watcher](../usage/watcher.md).

## Paths

```json
"TORRENT_ARCHIVE_PATH": "no_path",
```

Folder where the bot archives the generated `.torrent` files, organized in per-tracker subfolders (`<archive>/ITT/...`). With `no_path` it uses the default inside `Unit3Dup_config`.

## YouTube

```json
"YOUTUBE_FAV_CHANNEL_ID": "UC...",
"YOUTUBE_CHANNEL_ENABLE": "False",
"SKIP_YOUTUBE": "true",
"SKIP_TMDB": "false",
```

| Key | Effect |
|---|---|
| `YOUTUBE_FAV_CHANNEL_ID` | Favorite channel to pick trailers from |
| `YOUTUBE_CHANNEL_ENABLE` | Enables trailer search on the favorite channel |
| `SKIP_YOUTUBE` | Skips the YouTube trailer search entirely |
| `SKIP_TMDB` | Skips the TMDB lookup (not recommended for videos) |

## FAST_LOAD

```json
"FAST_LOAD": "0",
```

Limits how many items are processed per run (useful values: 1–150; `0` = no limit). Handy to test a `-scan` on a huge folder without processing all of it.

## Console colors (`console_options`)

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

Customize the console text and colors. Allowed colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, plus the `bold` variant (e.g. `"cyan bold"`).
