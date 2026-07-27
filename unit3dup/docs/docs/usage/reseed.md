# Reseed

`-reseed` puts **content you already have on disk** back into seeding, using torrents that already exist on the tracker — nothing new is created.

## How it works

```bash
unit3dup -reseed -f "/path/folder"
unit3dup -reseed -scan "/path/library"
```

For every video content found in the path:

1. The bot identifies the title (TMDB lookup, just like an upload)
2. It searches the tracker for a torrent **matching** your file
3. If found, it **downloads the `.torrent` from the tracker** into the [archive](../config/options.md#paths) (`<archive>/<TRACKER>/`)
4. It hands it to the torrent client, which resumes seeding using your local files

With multiple trackers (`MULTI_TRACKER` list or `-mt`) the round is repeated for each one.

## What it's for

- **Resume seeding** releases you had already uploaded, after switching client or machine
- **Seed existing releases** you already own identical files for
- **Migrate across OSes**: torrents created on Linux reseed on Windows and vice versa

!!! note "Video content only"
    Reseed works on movies and TV shows; documents and games are not involved.

!!! tip "Messy titles"
    If the folder name isn't enough to identify the title, add `-notitle "Real Title"`.
