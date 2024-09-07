## Unit3D_uploader
Unit3D platform uploader (Python >=3.10)

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

___
## Join Us

The program is functional but still in the early stages, undergoing constant modifications.
You can help improve this project or just hang out with us on
[discord](https://discord.gg/Pz3w5NNc) or [forum](https://itatorrents.xyz/forums/topics/414?page=1#post-1497) 

Thank you

___
## Use 'py' for windows , 'python3' for linux os
___

### Upload single episode or movie '-u' command
This command allows you to create and upload torrent for movies and series
and automatically upload and seed them.

python3 start.py -u "/home/uploader/myvideos/movie1.mkv

python3 start.py -u "/home/uploader/myvideos/S04E12.mkv

```
myvideos/
├── movie1.mkv
├── S04E12.mkv
```
### Upload multi-files and then multi-torrents
This command allows you to scan for movies and series and automatically upload and seed them.

python3 start.py -scan "/home/uploader/myvideos
```
myvideos/
├── movie1.mkv     
├── S04E12.mkv     
├── S01E01.mkv
├── movie2.mkv
├── S05E02.mkv
```
### Upload subfolders Movie and Serie
- `python3 start.py -scan "/home/uploader/myvideos
```
myvideos/
├── movie2/          
│   └── movie2.mkv
├── series1 S01/     
│   ├── S01E01.mkv
│   └── S01E02.mkv
├── series2 S01E02/  
│   └── S01E02.mkv 
```

### Upload subfolders and files Movie and Serie
- `python3 start.py -scan "/home/uploader/myvideos

```
myvideos/
├── movie1.mkv          
├── movie2/             
│   └── movie2.mkv
├── S04E12.mkv          
├── series1 S01/        
│   ├── S01E01.mkv
│   └── S01E02.mkv
├── series2 S01E02/     
│   └── S01E02.mkv 
```

### Install dependencies
 
- ffmpeg -version

If you have not installed ffmpeg install it:
- Linux : sudo apt install ffmpeg
- Windows : unzip https://www.ffmpeg.org/download.html and add its folder to
PATH environment user variable

### Bot Installation

1. Download the updater (zip) [Download autoupdate.py](https://gist.github.com/31December99/8e51466feb9df1606fd4199141ac54bb)
2. run python3 autoupdate.py
3. run pip install -r requirements.txt
4. Set up the configuration .env file(s) service and itt ( rename .back in .env)

### Update Bot 
python3 autoupdate.py

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
- duplicate_on=False
- number_of_screenshots=4
- torrent_archive =''
- preferred_lang=en
- size_th=100

let torrent_archive string empty or set your path if you want save torrent file inside

### Custom tracker .env file Example (itt.env):
- BASE_URL=https://...
- API_TOKEN=...


#### Searching:

    python3 start.py -s [title] (search by title)
    python3 start.py -i [title] (get info_hash and MediaInfo Unique ID)    
    python3 start.py -tmdb (search by TMDB ID)
    python3 start.py -torrent (create only the torrent file)
    python3 start.py -duplicate (force searching for duplicate)

    python3 start.py -up [username] (search by uploader's username)
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


### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.
