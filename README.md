
![Version](https://img.shields.io/badge/Unit3Dup-0.7.0-blue)
![Torrent Status](https://img.shields.io/badge/Online-green)
![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue)


## Auto Torrent Generator and Uploader

This Python script generates and uploads torrents based on input provided for movies or TV series and Games.

It performs the following tasks:

- Scan folder and subfolders
- Compiles various metadata information to create a torrent.
- Extracts a series of screenshots directly from the video.
- Extracts cover from the pdf documents 
- Generates meta-info derived from the video or Game.
- Searches for the corresponding ID on TMDB and IGDB.
- Add trailer from Tmdb or Youtube
- Seeding in qbittorrent or transmission

___
![Version](https://img.shields.io/badge/Flag_u-FILES-blue)

> **python3 start.py -u "/home/uploader/myvideos/Hello.world.S04E12.mkv"**

Output:

> Hello.world.S04E12.mkv.torrent

> **python3 start.py -u "/home/uploader/helloworld/Hello.world.book.pdf"**

Output:

> Hello.world.book.pdf.torrent

> **python3 start.py -u "/home/uploader/myvideos/Hello.world.TheMovie.mkv"**

Output:

> Hello.world.TheMovie.mkv.torrent


> **python3 start.py -u "/home/uploader/myvideos**

Output (only files):

> Hello.world.S04E12.mkv.torrent
> 
> Hello.world.book.pdf.torrent
> 
> Hello.world.TheMovie.mkv.torrent
> 
***

![Version](https://img.shields.io/badge/Flag_f-FOLDERS-blue)

> **python3 start.py -f "/home/uploader/Hello.world.S01**

>/home/uploader/Hello.world.S01E01
>
>/home/uploader/Hello.world.S01E02
>
>/home/uploader/Hello.world.S01E03

Output:

> Hello.world.S01.torrent
***

>python3 start.py -f "/home/uploader/Hello.world.S02E01**

Output:

>Hello.world.S02E01.torrent
***


**python3 start.py -f "/home/uploader/Hello.world.TheMovie**

Output:

>Hello.world.TheMovie.torrent
***


![Version](https://img.shields.io/badge/Flag_scan-FOLDERS_AND_FILES-blue)

> **python3 start.py -scan "/home/uploader/Archive**

Output:

> Hello.world.TheMovie.torrent
> 
> Hello.world.S02E01.torrent
> 
> Hello.world.TheBook.pdf.torrent
> 
> Hello.world.TheGame.torrent
***


![Version](https://img.shields.io/badge/Main_Flags-watcher-red)

![Version](https://img.shields.io/badge/watcher-red)

Every few seconds, it checks the watcher folder, moves the content to the watcher_destination, and uploads everything to the tracker. It won't upload if there's already a torrent file.

***

![Version](https://img.shields.io/badge/seedit-red)

Send the torrent file immediately to the default torrent client.
-seedit expects the media file path, not the torrent file path.


>**python3 start.py -seedit "/home/uploader/Hello.world.TheMovie**
***

![Version](https://img.shields.io/badge/force-red)

Unit3D as usual auto detects the media category but you can override it with the -force command

>**python3 start.py -force game -u "/home/uploader/Hello.world.pdf**

>**python3 start.py -force movie -f "/home/uploader/Hello.world**

You will get a message if you try to upload a game as a video or pdf
***

![Version](https://img.shields.io/badge/noseed-red)

Upload as usual but don't send the torrent file to the torrent client

>**python3 start.py -noseed -f "/home/uploader/Hello.world**
***

![Version](https://img.shields.io/badge/noup-red)

Don't upload and don't seed. Just create the file torrent

>**python3 start.py -noup -f "/home/uploader/Hello.world**
***


![Install](https://img.shields.io/badge/How_to_Install-gr) 

1.Download the last release (https://github.com/31December99/Unit3Dup/releases)

2. unzip it

3. pip install -r requirements.txt

4. python start.py



![Install](https://img.shields.io/badge/LINUX_ffmpeg-gr)

sudo apt install ffmpeg

![Install](https://img.shields.io/badge/WINDOWS_ffmpeg-gr)

Download and unzip https://www.ffmpeg.org/download.html and add its folder to
PATH environment user variable

![Install](https://img.shields.io/badge/QUICK_CONFIG-gr)


-> Linux : Unit3Dbot.json is located in the home directory on Linux

-> Windows: Unit3Dbot.json is located in the AppData folder on Windows

```
{
    "tracker_config": {
        "ITT_URL": "https://itatorrents.xyz",
        "ITT_APIKEY": "api_key12345",
        "ITT_PID": "pid_12345",
        "TMDB_APIKEY": "",
        "IMGBB_KEY": "",
        "FREE_IMAGE_KEY": "",
        "LENSDUMP_KEY": "",
        "PTSCREENS_KEY": "",
        "IMGFI_KEY": "",
        "YOUTUBE_KEY": "",
        "IGDB_CLIENT_ID": "",
        "IGDB_ID_SECRET": "",
    }
}
```

![Install](https://img.shields.io/badge/Upload_PDF-gr) 

unit3dup can grab the first page, convert it to an image (using xpdf),
and then the bot can upload it to an image host, then add the link to the torrent page description

### 

![Install](https://img.shields.io/badge/WINDOWS-Install_poppler_tools-gr)

1. Download and unzip poppler for windows from https://github.com/oschwartz10612/poppler-windows/releases
2. unzip it
2. Put the folder 'bin' in the system path. For example: C:\poppler-24.08.0\Library\bin
3. _close and reopen a new console window_
3. Test it: Run pdftocairo in the terminal

![Install](https://img.shields.io/badge/LINUX-Install_poppler_tools-gr)
1. sudo apt install poppler-utils
2. Test it: Run pdftocairo in the terminal

![Install](https://img.shields.io/badge/Bot_UPDATE-gr)

1. Delete only the bot folder
2. Download the release zip
3. Unzip it
4. no config
4. finish 


| Trackers          | Description              |
|-------------------|--------------------------|
| `ITT`             | https://itatorrents.xyz/ |



![Version](https://img.shields.io/badge/others-red)

| Flag               | Description           |
|--------------------|-----------------------|
| `-s`, `--search`   | Search for torrent    |
| `-i`, `--info`     | Get info on torrent   |
| `-up`, `--uploader`| Search by uploader    |
| `-desc`, `--description` | Search by description |
| `-bdinfo`, `--bdinfo`   | Show BDInfo           |
| `-m`, `--mediainfo`     | Show MediaInfo        |
| `-st`, `--startyear`    | Start year            |
| `-en`, `--endyear`      | End year              |
| `-type`, `--type`       | Filter by type        |
| `-res`, `--resolution`  | Filter by resolution  |
| `-file`, `--filename`   | Search by filename    |
| `-se`, `--season`       | Season number         |
| `-ep`, `--episode`      | Episode number        |
| `-tmdb`, `--tmdb_id`    | TMDB ID               |
| `-imdb`, `--imdb_id`    | IMDB ID               |
| `-tvdb`, `--tvdb_id`    | TVDB ID               |
| `-mal`, `--mal_id`      | MAL ID                |
| `-playid`, `--playlist_id` | Playlist ID         |
| `-coll`, `--collection_id` | Collection ID       |
| `-free`, `--freelech`   | Freelech discount     |
| `-a`, `--alive`         | Alive torrent         |
| `-d`, `--dead`          | Dead torrent          |
| `-dy`, `--dying`        | Dying torrent         |
***

## Join Us

The program is functional but still in the early stages, undergoing constant modifications.
You can help improve this project or just hang out with us on
[forum](https://itatorrents.xyz/forums/topics/414?page=1#post-1497)

[![Telegram](https://img.shields.io/badge/Telegram-contact-blue?style=for-the-badge&logo=telegram)](https://t.me/phantomdays)


Thank you