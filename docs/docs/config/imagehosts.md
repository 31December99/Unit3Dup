# Image hosts

The bot extracts screenshots from the video and uploads them to an image hosting service; the URLs end up in the torrent description. Keys live in `tracker_config`, priorities in `user_preferences`.

## Supported hosts

| Host | Site | Key |
|---|---|---|
| PtScreens | [ptscreens.com](https://ptscreens.com) | `PTSCREENS_KEY` |
| LensDump | [lensdump.com](https://lensdump.com) | `LENSDUMP_KEY` |
| FreeImage | [freeimage.host](https://freeimage.host) | `FREE_IMAGE_KEY` |
| ImgBB | [imgbb.com](https://imgbb.com) | `IMGBB_KEY` |
| ImgFI | [imgfi.com](https://imgfi.com) | `IMGFI_KEY` |
| PassIMA | [passtheima.ge](https://passtheima.ge) | `PASSIMA_KEY` |
| ImaRide | [imageride.net](https://www.imageride.net) | `IMARIDE_KEY` |

For each host: sign up on the site, generate the API key, paste it into `Unit3Dbot.json`:

```json
"IMGBB_KEY": "your_key",
"FREE_IMAGE_KEY": "your_key",
```

!!! tip "How many hosts should I configure?"
    You don't have to use them all, but **configure at least two**: if an upload to one host fails, the bot automatically moves to the next one.

## Priorities and fallback

In `user_preferences` every host has a priority — **0 = first attempt**:

```json
"PTSCREENS_PRIORITY": 0,
"LENSDUMP_PRIORITY": 1,
"FREE_IMAGE_PRIORITY": 2,
"IMGBB_PRIORITY": 3,
"IMGFI_PRIORITY": 4,
"PASSIMA_PRIORITY": 5,
"IMARIDE_PRIORITY": 6,
```

The bot tries the hosts in increasing priority order; on the first error (invalid key, service down, rate limit) it moves to the next one.

Screenshot options (`NUMBER_OF_SCREENSHOTS`, compression, resize, webp) are in [Advanced options](options.md).
