## Unit3D_uploader
Unit3D platform uploader (Python 3.10)

## Torrent Generator and Uploader

This Python script generates and uploads torrents based on input provided for movies or TV series.

It performs the following tasks:

- Scan subfolders
- Compiles various metadata information to create a torrent.
- Extracts a series of screenshots directly from the video.
- Generates meta-info derived from the video.
- Searches for the corresponding ID on TMDB (The Movie Database).
- Uploads the content to the UNIT3D Next Generation tracker platform.
- Seeding in qbittorrent

## Join Us

The program is functional but still in the early stages, undergoing constant modifications.
You can help improve this project or just hang out with us on
[Discord](https://discord.gg/CJ32Vwyu)

Thank you

___
### Example Usage

#### Config File Checking
- `python3 start.py -check  -> to verify configuration files`

#### Series 
- `python3 start.py -u "/home/uploader/myvideos/series1"

#### Movies
- `python3 start.py -u "/home/uploader/myvideos/TheMatrix.1080p.WEB-DL.H.264.mkv"`


#### In Manual Mode (-u):
This command allows you to create and upload torrent for movies and series
and automatically upload and seed them.

    Create a torrent for a single subfolder (series or movie).
    Create a torrent for a single movie or episode.
    Create a torrent file for a collection of files

#### In Auto Mode (-scan):
This command allows you to scan for movies and series and automatically upload and seed them.

    Create a torrent for each subfolder regardless of whether the subfolder
    contains a series or a movie.
    Create a torrent for a single episode.
    Create a torrent for one or more movies at once.

- `python3 start.py -scan /home/uploader/download`

```
download/
├── movie1.mkv          -> create a torrent
├── movie2/             -> create a torrent
│   └── movie2.mkv
├── S04E12.mkv          -> create a torrent
├── series1 S01/        -> create a torrent (pack)
│   ├── S01E01.mkv
│   └── S01E02.mkv
├── series2 S01E02/     -> create a torrent
│   └── S01E02.mkv 
```

#### Tracker (default itt)
- `python3 start.py -t mytracker -u /home/uploader/myvideos`

#### Searching (default itt)

    python3 start.py -s [title] (search by title)
    python3 start.py -up [username] (search by uploader's username)
    python3 start.py -i [title] (get info_hash and MediaInfo Unique ID)    
    python3 start.py -m [mediainfo_ID] (search by MediaInfo ID)
    python3 start.py -bdinfo [keyword] (search by bdinfo)
    python3 start.py -desc [keyword in description] (search by description)    
    python3 start.py -st [start_date] (search by starting date)
    python3 start.py -en [end_date] (search by ending date)
    python3 start.py -type (search by type ID)
    python3 start.py -res (search by resolution)
    python3 start.py -file (search by filename)
    python3 start.py -se (search by season number)
    python3 start.py -ep (search by episode number)
    python3 start.py -tmdb (search by TMDB ID)
    python3 start.py -imdb (search by IMDB ID)
    python3 start.py -tvdb (search by TVDB ID)
    python3 start.py -playid (search by playlist ID)    
    python3 start.py -coll (search by collection ID)
    python3 start.py -free (search by torrent's freeleech discount (0-100))
    python3 start.py -mal (search by MAL ID)
    python3 start.py -d (dead torrents)
    python3 start.py -dy (dying torrents)
    python3 start.py -a (alive torrent)
    python3 start.py -du (Double upload torrent)
    python3 start.py -fe (featured torrent)
    python3 start.py -str (stream-optimised torrent)
    python3 start.py -sd (Standard denition torrent)
    python3 start.py -hs (High speed torrent)
    python3 start.py -pers (personalRelease torrent)

___
### Dependencies
- requirements.txt
- apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
- apt-get install -y libmediainfo-dev

### Installation

1. Clone this repository.
2. Install the required dependencies using PIP.
3. Set up the configuration .env file(s) and remove the string '[Template]' from the file name
4. Run the script with python start.py

___
### Configuration

Make sure to configure the necessary API keys and authentication credentials in a separate configuration file (.env).

### Service.env file Example:

- API_TOKEN=...
- TMDB_APIKEY=...
- IMGBB_KEY=...
- QBIT_USER=... (username your qbittorrent client)
- QBIT_PASS=... (password your qbittorrent client)
- QBIT_URL=...  (url 127.0.0.1 local or remote ip)
- QBIT_PORT=... (port number check your qbit config.)

### Custom tracker .env file Example (itt.env):
- BASE_URL=https://...
- PASS_KEY=...
- API_TOKEN=...

___
### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.
