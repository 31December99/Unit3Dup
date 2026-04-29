# unit3dup CLI Documentation

Manage torrents, uploads, searches and configuration checks.

---

## Overview

`unit3dup` is a command-line tool for managing torrent uploads, searches, metadata filtering, and tracker operations.

---

## Usage

```bash
unit3dup [-h] [-check] [-u UPLOAD] [-f FOLDER] [-scan SCAN] [-b] [-reseed] [-watcher] [-notitle NOTITLE] [-tracker TRACKER] [-mt] [-force [FORCE]] [-noseed] [-noup] [-dup] [-personal] [-ftp] [-dmp] [-sch SEARCH] [-db]
        [-i INFO] [-up UPLOADER] [-d DESCRIPTION] [-bd BDINFO] [-m MEDIAINFO] [-st STARTYEAR] [-en ENDYEAR] [-type TYPE] [-res RESOLUTION] [-file FILENAME] [-se SEASON] [-ep EPISODE] [-tmdb TMDB_ID] [-imdb IMDB_ID]
        [-tvdb TVDB_ID] [-mal MAL_ID] [-playid PLAYLIST_ID] [-coll COLLECTION_ID] [-free FREELECH] [-al] [-dd] [-dy] [-du] [-fe] [-re] [-str] [-sd] [-hs] [-int] [-pr]
```

---

## Config Commands

### `-check, --check`

Check configuration files and environment setup.

---

## Upload Commands

### Upload & Input

* `-u, --upload` → Upload path
* `-f, --folder` → Upload folder
* `-scan, --scan` → Scan folder

### Processing

* `-b, --buildtags` → Auto build title/tags
* `-reseed, --reseed` → Reseed existing torrent
* `-watcher, --watcher` → Start watcher service

### Metadata

* `-notitle, --notitle` → Manual title override
* `-tracker, --tracker` → Target tracker
* `-mt, --mt` → Multi tracker upload
* `-force [FORCE]` → Force category selection

### Upload Control

* `-noseed, --noseed` → Disable seeding
* `-noup, --noup` → Create torrent only
* `-dup, --duplicate` → Detect duplicates
* `-personal, --personal` → Mark as personal release
* `-ftp, --ftp` → Enable FTP connection

---

## Search Commands

* `-dmp, --dump` → Dump all titles
* `-sch, --search` → Search torrents
* `-db, --dbsave` → Save results
* `-i, --info` → Torrent information
* `-up, --uploader` → Filter by uploader
* `-d, --description` → Search by description
* `-bd, --bdinfo` → Show BDInfo
* `-m, --mediainfo` → Show MediaInfo

---

## Filter Options

### Time Filters

* `-st, --startyear` → Start year
* `-en, --endyear` → End year

### Media Filters

* `-type` → Content type
* `-res, --resolution` → Resolution
* `-file, --filename` → Filename
* `-se, --season` → Season
* `-ep, --episode` → Episode

### IDs

* `-tmdb` → TMDB ID
* `-imdb` → IMDB ID
* `-tvdb` → TVDB ID
* `-mal` → MAL ID
* `-playid` → Playlist ID
* `-coll` → Collection ID

### Status Filters

* `-free` → Freeleech
* `-al` → Alive
* `-dd` → Dead
* `-dy` → Dying

---

## Special Flags

* `-du` → DoubleUp
* `-fe` → Featured
* `-re` → Refundable
* `-str` → Stream enabled
* `-sd` → Standard definition
* `-hs` → Highspeed
* `-int` → Internal release
* `-pr` → Personal release

---

## Example

```bash
unit3dup -mt -b -u "/home/parzival/TEST/scan/007 - Vivi e lascia morire (1973) .mkv FullHD 1080p HEVC x265 AC3 ITA-ENG.mkv"
```

Scan folder, auto-generate tags, upload to multiple trackers.
