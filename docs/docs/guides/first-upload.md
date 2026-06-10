# First upload step by step

From zero to your first torrent on ITT. Estimated time: 15 minutes.

## 1. Install

Follow the page for your system: [Windows](../install/windows.md) · [Linux](../install/linux.md) · [ultra.cc seedbox](../install/seedbox.md).

Then launch the bot once so it creates its configuration files:

```bash
unit3dup
```

Red messages are expected: the bot isn't configured yet.

## 2. Configure the bare minimum

Open `Unit3Dbot.json` (Windows: `%LOCALAPPDATA%\Unit3Dup_config\` — Linux: `~/Unit3Dup_config/`) and fill in these fields:

```json
{
    "tracker_config": {
        "ITT_URL": "https://itatorrents.xyz",
        "ITT_APIKEY": "your_api_key",
        "ITT_PID": "your_passkey",
        "MULTI_TRACKER": ["itt"],
        "TMDB_APIKEY": "your_tmdb_key",
        "IMGBB_KEY": "your_imgbb_key",
        "FREE_IMAGE_KEY": "your_freeimage_key"
    },
    "torrent_client_config": {
        "QBIT_USER": "admin",
        "QBIT_PASS": "your_password",
        "QBIT_HOST": "127.0.0.1",
        "QBIT_PORT": "8080",
        "TORRENT_CLIENT": "qbittorrent"
    }
}
```

(All the other sections and keys stay as they are.)

Where to find each value:

- **ITT API key and PID** → on the tracker, in your profile settings ([details](../config/trackers.md))
- **TMDB** → free account at [themoviedb.org](https://www.themoviedb.org/) → Settings → API ([details](../config/metadata.md))
- **Image hosts** → sign up at [imgbb.com](https://imgbb.com) and [freeimage.host](https://freeimage.host), generate the keys ([details](../config/imagehosts.md))
- **qBittorrent** → WebUI credentials ([details](../config/clients.md))

!!! tip "Trimmed MULTI_TRACKER"
    `"MULTI_TRACKER": ["itt"]` with just your tracker: you avoid PID errors for trackers you don't use.

## 3. Check

```bash
unit3dup -check
```

If something is wrong, the bot tells you which field to fix.

## 4. First upload

Pick a test video file that follows the tracker rules, then:

```bash
unit3dup -u "/path/to/movie.mkv"
```

What happens, in order:

1. **Analysis** — the bot inspects the file and prints the processing table
2. **Metadata lookup** — it queries TMDB and proposes the title ID
3. **Screenshots** — it extracts images from the video and uploads them to the image host
4. **Torrent** — it generates the `.torrent` and stores it in the archive (`torrent_archive_path/ITT/`)
5. **Upload** — it sends everything to the tracker and receives the page link
6. **Seeding** — it hands the torrent to qBittorrent, which starts seeding right away

## 5. Check the result

- The torrent page on the tracker: title, tags, screenshots, mediainfo
- qBittorrent: the torrent must be seeding with the label set in `TAG`

All good? Done. Next steps: [Basic upload](../usage/upload.md) for `-f` and `-scan`, [Tags and titles](../usage/tags.md) to polish your titles, [Multi-tracker](../usage/multitracker.md) to upload everywhere.
