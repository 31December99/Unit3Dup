# Configuration — getting started

## Where the configuration lives

On **first run** the bot creates the `Unit3Dup_config` folder containing the main configuration file and the support files:

| System | Path |
|---|---|
| Windows | `%LOCALAPPDATA%\Unit3Dup_config\` |
| Linux / macOS | `~/Unit3Dup_config/` |

Folder contents:

| File | Purpose |
|---|---|
| `Unit3Dbot.json` | **Main configuration**: trackers, API keys, torrent client, preferences |
| `tags_list.json` | Custom tags for title building ([details](../usage/tags.md)) |
| `sign_list.json` | Releaser signatures ([details](../usage/tags.md)) |
| `ban_list.json` | Words to strip from titles ([details](../usage/tags.md)) |

!!! warning "The file is named `Unit3Dbot.json`"
    Older versions of the documentation called it "Unit3D.json": the correct name is **`Unit3Dbot.json`**.

In the same folder the bot also creates the default subfolders `torrent_archive_path` (where generated `.torrent` files are stored), `cache_path`, `watcher_path` and `watcher_destination_path` — all customizable (see [Advanced options](options.md)).

## File structure

`Unit3Dbot.json` is split into **five sections**:

```json
{
    "tracker_config": { },
    "torrent_client_config": { },
    "user_preferences": { },
    "options": { },
    "console_options": { }
}
```

| Section | Contents | Page |
|---|---|---|
| `tracker_config` | Tracker URLs and API keys, TMDB/TVDB/IGDB/YouTube keys, image host keys | [Trackers](trackers.md), [Metadata](metadata.md), [Image hosts](imagehosts.md) |
| `torrent_client_config` | qBittorrent, Transmission, rTorrent | [Torrent clients](clients.md) |
| `user_preferences` | Screenshots, cache, watcher, duplicates, tags, language… | [Advanced options](options.md) |
| `options` | FTP connection | [FTP](../usage/ftp.md) |
| `console_options` | Console colors and messages | [Advanced options](options.md) |

## Minimal configuration

You don't need to fill in every line. To get started you only need:

1. **`ITT_URL` + `ITT_APIKEY`** (or your tracker) — [Trackers](trackers.md)
2. **`TMDB_APIKEY`** — [Metadata](metadata.md)
3. **At least two image host keys** — [Image hosts](imagehosts.md)
4. **`TORRENT_CLIENT` + client credentials** — [Torrent clients](clients.md)

Unconfigured values stay `no_key` / `no_pass` / `no_path`.

## Check your configuration

```bash
unit3dup -check
```

It validates the configuration files and the environment. On startup the bot always prints the active paths:

```text
[Configuration] '~/Unit3Dup_config/Unit3Dbot.json'
[*.torrent Archive] '~/Unit3Dup_config/torrent_archive_path'
[Images,Tmdb cache] '~/Unit3Dup_config/cache_path'
[Watcher] '~/Unit3Dup_config/watcher_path'
[Watcher] '~/Unit3Dup_config/watcher_destination_path'
[Preferred Language] 'all'
```

!!! danger "Blocking errors"
    If a value is malformed the bot exits immediately with a message like `-> Please Fix 'FIELD' ['value'] in settings.json`: open `Unit3Dbot.json` and fix the reported field.
