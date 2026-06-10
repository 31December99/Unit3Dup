# Installation on Windows

## Requirements

- **Python 3.10 or newer** (recommended: 3.10 to 3.12 — newer versions may have issues with some libraries)
- **FFmpeg** — used to extract screenshots from videos
- **Poppler** — only if you want to create torrents for PDF documents

## 1. Install FFmpeg

1. Download FFmpeg from [ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)
2. Unzip the archive to a folder of your choice (e.g. `C:\ffmpeg`)
3. Add the FFmpeg `bin` folder to your **PATH** environment variable (user)
4. Close and reopen the terminal, then verify:

```bash
ffmpeg -version
```

## 2. Poppler (PDF only)

Needed only if you upload PDF documents — the bot uses it to extract the cover from the first page.

1. Download Poppler for Windows from [github.com/oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Unzip it and add the `bin` folder to the system PATH (example: `C:\poppler-24.08.0\Library\bin`)
3. **Close and reopen the terminal**
4. Verify the installation:

```bash
pdftocairo -v
```

## 3. Install Unit3Dup

```bash
pip install unit3dup
```

## 4. First run

```bash
unit3dup
```

!!! note "Red messages on first run?"
    That's expected: the bot is telling you it's not configured yet. On first run it creates the configuration folder and the `Unit3Dbot.json` file. Continue with the [Configuration](../config/intro.md).
