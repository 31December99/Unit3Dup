# FTP

With `-ftp` the bot connects to a remote FTP server, lets you **browse and pick files** from an interactive menu, downloads them locally and uploads them to the tracker.

## Configuration

`options` section of `Unit3Dbot.json`:

```json
"options": {
    "FTPX_USER": "user",
    "FTPX_PASS": "pass",
    "FTPX_IP": "127.0.0.1",
    "FTPX_PORT": 2121,
    "FTPX_LOCAL_PATH": "/local/download/path",
    "FTPX_ROOT": ".",
    "FTPX_KEEP_ALIVE": "False"
}
```

| Key | Meaning |
|---|---|
| `FTPX_USER` / `FTPX_PASS` | FTP server credentials |
| `FTPX_IP` / `FTPX_PORT` | Server address and port |
| `FTPX_LOCAL_PATH` | Local folder for downloads |
| `FTPX_ROOT` | Remote starting folder |
| `FTPX_KEEP_ALIVE` | Keeps the connection alive |

## Usage

```bash
unit3dup -ftp
```

1. The bot connects and shows the remote folder contents as a **numbered table**
2. You navigate: pick a folder to enter it, a file to download it
3. `0` to quit
4. On exit, if you downloaded something: any **`.rar` archives are extracted** automatically, then the downloaded content gets uploaded (like [`-f`](upload.md))

!!! tip "Remote seedbox"
    Typical use case: you grab releases from your seedbox over FTP and upload them to the tracker from your home machine, no manual steps.
