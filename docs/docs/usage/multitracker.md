# Multi-tracker

The bot can upload the same content to a single tracker or to every tracker configured in `MULTI_TRACKER` ([configuration](../config/trackers.md)).

## `-tracker` — one specific tracker

```bash
unit3dup -tracker ptt -u "/path/movie.mkv"
```

Uploads only to the given tracker. The name must be in the `MULTI_TRACKER` list, otherwise:

```text
Tracker 'xyz' not found. Please update your configuration file
```

Without `-tracker`, the bot uses the **first tracker in the list** — this also applies to all [search](search.md) commands.

## `-mt` — all trackers

```bash
unit3dup -mt -u "/path/movie.mkv"
```

Uploads to **all** the trackers in `MULTI_TRACKER`, one after the other: for each it builds the torrent with the right announce URL, uploads it and starts seeding.

On startup the bot checks that every tracker responds:

```text
Tracker -> 'ITT' Online
Tracker -> 'PTT' Online
```

!!! warning "Every tracker needs its PID"
    Each tracker in `MULTI_TRACKER` must have both `*_APIKEY` **and** `*_PID` configured: without the PID the bot exits with `-> No PID value`. If you don't use a tracker, remove it from the list.
