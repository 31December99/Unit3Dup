# Torrent clients

`torrent_client_config` section of `Unit3Dbot.json`. After the upload, the bot hands the torrent to your client for **seeding**.

## Pick your client

```json
"TORRENT_CLIENT": "qbittorrent",
```

Allowed values: `qbittorrent`, `transmission`, `rtorrent`.

The client is **required** for any upload with seeding (`-u`, `-f`, `-scan`, `-watcher`, `-reseed`): on startup the bot tests the connection and exits with `Unknown Torrent Client name` or a connection error if something is wrong.

!!! tip "No client?"
    With `-noseed` (upload without seeding) or `-noup` (create the `.torrent` only) the client is never contacted.

## qBittorrent

```json
"QBIT_USER": "admin",
"QBIT_PASS": "your_password",
"QBIT_HOST": "127.0.0.1",
"QBIT_PORT": "8080",
"SHARED_QBIT_PATH": "no_path",
```

**WebUI** credentials (in qBittorrent: *Tools → Options → WebUI*). `QBIT_HOST` takes the IP of the machine running the client.

## Transmission

```json
"TRASM_USER": "admin",
"TRASM_PASS": "your_password",
"TRASM_HOST": "127.0.0.1",
"TRASM_PORT": "9091",
"SHARED_TRASM_PATH": "no_path",
```

## rTorrent

```json
"RTORR_USER": "admin",
"RTORR_PASS": "your_password",
"RTORR_HOST": "127.0.0.1",
"RTORR_PORT": "9091",
"SHARED_RTORR_PATH": "no_path",
```

## SHARED_*_PATH — client on another machine

If your torrent client runs on a **different** machine, container or OS than the one running the bot, your local file paths won't match what the client sees.

`SHARED_*_PATH` is the path **as seen by the client**: the bot uses it instead of the local path when registering the torrent for seeding.

Example — bot on Windows, qBittorrent in a container mounting the same folder at `/downloads`:

```json
"SHARED_QBIT_PATH": "/downloads",
```

## TAG

```json
"TAG": "ADDED TORRENTS",
```

Label/category applied to the torrents the bot adds to the client: handy to spot and filter them.
