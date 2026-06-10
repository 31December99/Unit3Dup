# Watcher

The watcher is the **automatic** mode: the bot monitors a folder and uploads to the tracker everything that lands in it. Great paired with a client downloading to a fixed folder.

## Start

```bash
unit3dup -watcher
```

The flag takes no parameters: everything is configured in `Unit3Dbot.json`.

## Configuration

In `user_preferences` ([Advanced options](../config/options.md#watcher)):

```json
"WATCHER_INTERVAL": 60,
"WATCHER_PATH": "/path/source/folder",
"WATCHER_DESTINATION_PATH": "/path/destination/folder",
```

- `WATCHER_PATH` → the **watched** folder (e.g. where files get downloaded)
- `WATCHER_DESTINATION_PATH` → the folder where files are **moved** and uploaded from
- `WATCHER_INTERVAL` → how many **seconds** between checks

## What happens on every cycle

When `WATCHER_INTERVAL` expires (you see the countdown on screen):

1. It checks `WATCHER_PATH`; if empty, the countdown restarts
2. It **moves** all files to `WATCHER_DESTINATION_PATH`, preserving subfolders (emptied folders are removed)
3. It processes the moved files and **uploads them to the tracker** with seeding, like a [`-scan`](upload.md)
4. It starts over

The loop is endless: exit with ++ctrl+c++.

!!! warning "Files are moved, not copied"
    `WATCHER_PATH` gets **emptied** on every cycle. Don't point it to a folder whose files must stay where they are (e.g. your client's seeding folder).

!!! tip "Folder missing?"
    If `WATCHER_PATH` doesn't exist or isn't configured, the bot stops with `Watcher path does not exist or is not configured`.
