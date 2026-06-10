# Tags and titles

The torrent title is made of the **media title** plus a set of **tags** derived from the file analysis: resolution, source, audio/video codec, language, HDR…

Available tags: `version`, `resolution`, `uhd`, `platform`, `source`, `remux`, `multi`, `acodec`, `channels`, `flag`, `subtitle`, `vcodec`, `hdr`, `video_encoder`.

## `-b` — rebuild the title

```bash
unit3dup -b -u "/path/movie.mkv"
```

With `-b/--buildtags` the bot **rebuilds from scratch** the title and tags using the technical analysis of the media (MediaInfo) and the file name, in the order defined by `TAGS_POSITION_MOVIE` / `TAGS_POSITION_SERIE` ([Advanced options](../config/options.md#tag-order-in-the-title)).

It **does not rename your file**: it only builds the torrent title shown on the tracker page.

Without `-b`, the title stays closer to the original file name.

## The three customization files

They live in the configuration folder (`Unit3Dup_config`) and are created on first run with default values. They are plain JSON, editable with any text editor.

### `tags_list.json` — custom tags

Maps **word → tag type**: it teaches the bot to recognize words in file names and classify them.

```json
{
    "REMUX": "remux",
    "WEB-DL": "source",
    "AMZN": "platform"
}
```

Used by `-b`: when the word appears in the file name, the value lands in the right tag of the title. You can add your own entries (e.g. release group names or unusual sources).

!!! warning "Required by `-b`"
    If `tags_list.json` is missing, the bot reports it at startup when you use `-b`.

### `ban_list.json` — tags to exclude from the autobuild

Excludes entire **tag types** from the title rebuild: a tag listed here never ends up in the title built by `-b`. Keys are the tag names (the same ones used in `TAGS_POSITION_*`); the value is just a placeholder.

Example — never include the video codec nor the encoder in the title:

```json
{
    "vcodec": "banned",
    "video_encoder": "banned"
}
```

### `sign_list.json` — releaser signatures

List of signatures recognized as **release groups**. Together with `RELEASER_SIGN` ([Advanced options](../config/options.md#language-anonymity-and-signature)) it manages the signature at the end of the title (max 20 characters, special characters stripped).

## Manual title

When the file name is too messy to extract a title from (typical with season packs without a title):

```bash
unit3dup -u "/path/S01.pack.1080p.mkv" -notitle "Show Name"
```

`-notitle` forces the title used for the **TMDB search**, without touching the technical tags.
