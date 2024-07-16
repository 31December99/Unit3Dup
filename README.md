## Unit3D_uploader
Unit3D platform uploader

## Torrent Generator and Uploader

The program is functional but still in an early stage, undergoing constant modifications.

This Python script generates and uploads torrents based on input provided for movies or TV series. It performs the following tasks:

- Compiles various metadata information to create a torrent.
- Extracts a series of screenshots directly from the video.
- Generates meta-info derived from the video.
- Searches for the corresponding ID on TMDB (The Movie Database).
- Uploads the content to the UNIT3D Next Generation tracker platform.
- Seeding in qbittorrent

___
### Example Usage

#### Series 
- `python3 start.py -u /home/uploader/myvideos  -> use only folder for series`

#### Movies
- `python3 start.py -u /home/uploader/myvideos/TheMatrix.1080p.WEB-DL.H.264.mkv`

#### Tracker (default itt)
- `python3 start.py -t mytracker -u /home/uploader/myvideos`

#### Searching (default itt)

    python3 start.py -s [title] (search by title)
    python3 start.py -i [title] (get info_hash and MediaInfo Unique ID)
    python3 start.py -up [username] (search by uploader's username)
    python3 start.py -m [mediainfo_ID] (search by MediaInfo ID)
    python3 start.py -st [start_date] (search by starting date)
    python3 start.py -en [end_date] (search by ending date)
    python3 start.py -type (search by type ID)
    python3 start.py -res (search by resolution)
    python3 start.py -tmdb (search by TMDB ID)
    python3 start.py -imdb (search by IMDB ID)
    python3 start.py -tvdb (search by TVDB ID)
    python3 start.py -d (dead torrents)
    python3 start.py -dy (dying torrents)
    python3 start.py -a (alive torrent)
___
### Dependencies
- requirements.txt
- apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
- apt-get install -y libmediainfo-dev

### Installation

1. Clone this repository.
2. Install the required dependencies using PIP.
3. Config address and port for qbittorrent webui
4. Set the configuration .env file
5. Run the script with python start.py

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
