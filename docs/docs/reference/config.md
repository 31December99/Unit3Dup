# Full config reference

Every key of `Unit3Dbot.json`, section by section. "Default" is the value in the file generated on first run; the `no_key` / `no_pass` / `no_path` placeholders mean "not configured".

## `tracker_config`

| Key | Type | Default | Required | Description |
|---|---|---|---|---|
| `ITT_URL` | string | `https://itatorrents.xyz` | to use ITT | ITT tracker URL |
| `ITT_APIKEY` | string | `no_key` | to use ITT | Your ITT profile API key |
| `ITT_PID` | string | `no_key` | if `itt` is in `MULTI_TRACKER` | ITT passkey |
| `SIS_URL` | string | `https://no_tracker.xyz` | to use SIS | SIS tracker URL |
| `SIS_APIKEY` | string | `no_key` | to use SIS | SIS API key |
| `SIS_PID` | string | `no_key` | if `sis` is in `MULTI_TRACKER` | SIS passkey |
| `PTT_URL` | string | `https://polishtorrent.top` | to use PTT | PTT tracker URL |
| `PTT_APIKEY` | string | `no_key` | to use PTT | PTT API key |
| `PTT_PID` | string | `no_key` | if `ptt` is in `MULTI_TRACKER` | PTT passkey |
| `AST_URL` | string | `https://arabicsource.net` | to use AST | AST tracker URL |
| `AST_APIKEY` | string | `no_key` | to use AST | AST API key |
| `AST_PID` | string | `no_key` | if `ast` is in `MULTI_TRACKER` | AST passkey |
| `MULTI_TRACKER` | list | `["itt","sis","ptt","ast"]` | yes (non-empty) | Active trackers; the first is the default. No duplicates |
| `TMDB_APIKEY` | string | `no_key` | for videos | TheMovieDB key |
| `TVDB_APIKEY` | string | `no_key` | recommended for TV shows | TheTVDB key |
| `IMGBB_KEY` | string | `no_key` | at least one host | ImgBB key |
| `FREE_IMAGE_KEY` | string | `no_key` | at least one host | FreeImage key |
| `LENSDUMP_KEY` | string | `no_key` | at least one host | LensDump key |
| `PTSCREENS_KEY` | string | `no_key` | at least one host | PtScreens key |
| `IMGFI_KEY` | string | `no_key` | at least one host | ImgFI key |
| `PASSIMA_KEY` | string | `no_key` | at least one host | PassIMA key |
| `IMARIDE_KEY` | string | `no_key` | at least one host | ImaRide key |
| `YOUTUBE_KEY` | string | `no_key` | no | YouTube Data API key (trailers) |
| `IGDB_CLIENT_ID` | string | `no_key` | for games | IGDB/Twitch Client ID |
| `IGDB_ID_SECRET` | string | `no_key` | for games | IGDB/Twitch Client Secret |

## `torrent_client_config`

| Key | Type | Default | Required | Description |
|---|---|---|---|---|
| `QBIT_USER` | string | `admin` | if using qBittorrent | WebUI username |
| `QBIT_PASS` | string | `no_pass` | if using qBittorrent | WebUI password |
| `QBIT_HOST` | string | `127.0.0.1` | if using qBittorrent | Client host |
| `QBIT_PORT` | number | `8080` | if using qBittorrent | WebUI port |
| `SHARED_QBIT_PATH` | string | `no_path` | no | Path as seen by the client when it runs elsewhere |
| `TRASM_USER` | string | `admin` | if using Transmission | Username |
| `TRASM_PASS` | string | `no_pass` | if using Transmission | Password |
| `TRASM_HOST` | string | `127.0.0.1` | if using Transmission | Host |
| `TRASM_PORT` | number | `9091` | if using Transmission | Port |
| `SHARED_TRASM_PATH` | string | `no_path` | no | Path as seen by the client when it runs elsewhere |
| `RTORR_USER` | string | `admin` | if using rTorrent | Username |
| `RTORR_PASS` | string | `no_pass` | if using rTorrent | Password |
| `RTORR_HOST` | string | `127.0.0.1` | if using rTorrent | Host |
| `RTORR_PORT` | number | `9091` | if using rTorrent | Port |
| `SHARED_RTORR_PATH` | string | `no_path` | no | Path as seen by the client when it runs elsewhere |
| `TORRENT_CLIENT` | string | `qbittorrent` | for uploads with seeding | `qbittorrent`, `transmission` or `rtorrent` |
| `TAG` | string | `ADDED TORRENTS` | no | Label applied to torrents in the client |

## `user_preferences`

| Key | Type | Default | Description |
|---|---|---|---|
| `PTSCREENS_PRIORITY` | number | `0` | Image host priority (0 = first) |
| `LENSDUMP_PRIORITY` | number | `1` | LensDump priority |
| `FREE_IMAGE_PRIORITY` | number | `2` | FreeImage priority |
| `IMGBB_PRIORITY` | number | `3` | ImgBB priority |
| `IMGFI_PRIORITY` | number | `4` | ImgFI priority |
| `PASSIMA_PRIORITY` | number | `5` | PassIMA priority |
| `IMARIDE_PRIORITY` | number | `6` | ImaRide priority |
| `NUMBER_OF_SCREENSHOTS` | number | `4` | Screenshots extracted from the video (2–10) |
| `TAGS_POSITION_MOVIE` | list | see [Options](../config/options.md#tag-order-in-the-title) | Tag order in movie titles (5–17 entries) |
| `TAGS_POSITION_SERIE` | list | see [Options](../config/options.md#tag-order-in-the-title) | Tag order in TV show titles |
| `YOUTUBE_FAV_CHANNEL_ID` | string | ITT channel | Favorite YouTube channel for trailers |
| `YOUTUBE_CHANNEL_ENABLE` | boolean | `False` | Enables the favorite-channel search |
| `DUPLICATE_ON` | boolean | `true` | Duplicate check on every upload |
| `SKIP_DUPLICATE` | boolean | `false` | Skips duplicate content without asking |
| `SKIP_TMDB` | boolean | `false` | Skips the TMDB lookup |
| `SKIP_YOUTUBE` | boolean | `true` | Skips the YouTube trailer search |
| `SIZE_TH` | number | `10` | Size difference % threshold for duplicate matching |
| `WATCHER_INTERVAL` | number | `60` | Seconds between watcher checks |
| `WATCHER_PATH` | string | `no_path` | Folder watched by the watcher |
| `WATCHER_DESTINATION_PATH` | string | `no_path` | Watcher file destination |
| `TORRENT_ARCHIVE_PATH` | string | `no_path` | Archive of the generated `.torrent` files |
| `CACHE_PATH` | string | `no_path` | Cache folder |
| `COMPRESS_SCSHOT` | number | `3` | Screenshot compression |
| `RESIZE_SCSHOT` | boolean | `False` | Resizes screenshots |
| `TORRENT_COMMENT` | string | `no_comment` | Comment inside the `.torrent` file |
| `PREFERRED_LANG` | string | `all` | Preferred language (ISO 3166) or `all` |
| `ANON` | boolean | `False` | Anonymous upload |
| `WEBP_ENABLED` | boolean | `False` | Animated webp in the description |
| `CACHE_SCR` | boolean | `False` | Screenshot cache |
| `CACHE_DBONLINE` | boolean | `False` | Online search cache |
| `PERSONAL_RELEASE` | boolean | `False` | Personal release on every upload |
| `FAST_LOAD` | number | `0` | Caps the processed items (1–150; 0 = all) |
| `RELEASER_SIGN` | string | empty | Releaser signature (max 20 characters) |

## `options`

| Key | Type | Default | Description |
|---|---|---|---|
| `FTPX_USER` | string | `user` | FTP username |
| `FTPX_PASS` | string | `pass` | FTP password |
| `FTPX_IP` | string | `127.0.0.1` | FTP server IP |
| `FTPX_PORT` | number | `2121` | FTP port |
| `FTPX_LOCAL_PATH` | string | `.` | Local download folder |
| `FTPX_ROOT` | string | `.` | Remote starting folder |
| `FTPX_KEEP_ALIVE` | boolean | `False` | Keeps the connection alive |

## `console_options`

| Key | Type | Default | Description |
|---|---|---|---|
| `NORMAL_COLOR` | string | `blue bold` | Normal message color |
| `ERROR_COLOR` | string | `red bold` | Error color |
| `WELCOME_MESSAGE` | string | `https://itatorrents.xyz` | Welcome banner text |
| `WELCOME_MESSAGE_COLOR` | string | `blue` | Banner color |
| `WELCOME_MESSAGE_BORDER_COLOR` | string | `yellow` | Banner border |
| `PANEL_MESSAGE_COLOR` | string | `blue` | Panel color |
| `PANEL_MESSAGE_BORDER_COLOR` | string | `yellow` | Panel border |
| `QUESTION_MESSAGE_COLOR` | string | `yellow` | Question color |

Allowed colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` (+ ` bold`).

Boolean values accept `true`/`false`, `1`/`0`, `yes`/`no` (as strings or native).
