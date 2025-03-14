
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

**python3 start.py -u "/home/uploader/myvideos/Hello.world.S04E12.mkv"**

Output:

![Version](https://img.shields.io/badge/Hello.world.S04E12.mkv.torrent-brown)

**python3 start.py -u "/home/uploader/helloworld/Hello.world.book.pdf"**

Output:

![Version](https://img.shields.io/badge/Hello.world.book.pdf.torrent-brown)

**python3 start.py -u "/home/uploader/myvideos/Hello.world.TheMovie.mkv"**

Output:

![Version](https://img.shields.io/badge/Hello.world.TheMovie.mkv.torrent-brown)

There is no difference between movie, series, and game, but there is a difference between folders and files:

**python3 start.py -u "/home/uploader/myvideos**

Output:

![Version](https://img.shields.io/badge/Hello.world.S04E12.mkv.torrent-brown)
![Version](https://img.shields.io/badge/Hello.world.book.pdf.torrent-brown)
![Version](https://img.shields.io/badge/Hello.world.TheMovie.mkv.torrent-brown)


![Version](https://img.shields.io/badge/Flag_f-FOLDERS-blue)

**python3 start.py -f "/home/uploader/Hello.world.S01**

/home/uploader/Hello.world.S01E01

/home/uploader/Hello.world.S01E02

/home/uploader/Hello.world.S01E03

etc..

Output:

![Version](https://img.shields.io/badge/Hello.world.S01.torrent-brown)

***
**python3 start.py -f "/home/uploader/Hello.world.S02E01**

Output:

![Version](https://img.shields.io/badge/Hello.world.S02E01.torrent-brown)
***


**python3 start.py -f "/home/uploader/Hello.world.TheMovie**

Output:

![Version](https://img.shields.io/badge/Hello.world.TheMovie.torrent-brown)
***


![Version](https://img.shields.io/badge/Flag_scan-FOLDERS_AND_FILES-blue)

**python3 start.py -scan "/home/uploader/Archive**

Output:

![Version](https://img.shields.io/badge/Hello.world.TheMovie.torrent-brown)
![Version](https://img.shields.io/badge/Hello.world.S02E01.torrent-brown)
![Version](https://img.shields.io/badge/Hello.world.TheBook.pdf.torrent-brown)
![Version](https://img.shields.io/badge/Hello.world.TheGame.torrent-brown)
***


![Version](https://img.shields.io/badge/Main_Flags-watcher-red)

![Version](https://img.shields.io/badge/watcher-red)

Every few seconds, it checks the watcher folder, moves the content to the watcher_destination, and uploads everything to the tracker. It won't upload if there's already a torrent file.

![Version](https://img.shields.io/badge/tracker-red)

You can select a specific tracker name that has been configured in the configuration file *.json

If you don't specify any tracker, the default tracker will be the first one in the list in the configuration file

Default tracker:

**python3 start.py -u "/home/uploader/Hello.world.TheBook.pdf**

Specified tracker:

**python3 start.py -tracker itt -f "/home/uploader/Hello.world.TheMovie**

**python3 start.py -tracker itt -u "/home/uploader/Hello.world.TheBook.pdf**

**python3 start.py -tracker partner -u "/home/uploader/Hello.world.TheBook.pdf**

When you use -tracker , the tracker of the torrent file will be updated with the 'partner' URL announcement,

so you need to configure your passkey in the configuration JSON file


![Version](https://img.shields.io/badge/cross-red)

Add all the trackers that have been configured in the JSON file to a specified torrent file

-cross expects the media file path, not the torrent file path.
Therefore, it checks the torrent archive to see if the file exists and edits it.

**python3 start.py -cross -f "/home/uploader/Hello.world.TheMovie**
verificare
***

![Version](https://img.shields.io/badge/seedit-red)

Send the torrent file immediately to the default torrent client.
-seedit expects the media file path, not the torrent file path.


**python3 start.py -seedit "/home/uploader/Hello.world.TheMovie**


![Version](https://img.shields.io/badge/force-red)

Unit3D as usual auto detects the media category but you can override it with the -force command

**python3 start.py -force game -u "/home/uploader/Hello.world.pdf**

**python3 start.py -force movie -f "/home/uploader/Hello.world**

You will get an error from MediaInfo if you try to upload a game as a video or pdf


![Version](https://img.shields.io/badge/noseed-red)

Upload as usual but don't send the torrent file to the torrent client

**python3 start.py -noseed -f "/home/uploader/Hello.world**


![Version](https://img.shields.io/badge/noup-red)

Don't upload and don't seed. Just create the file torrent

**python3 start.py -noup -f "/home/uploader/Hello.world**

**python3 start.py -tracker itt -noup -f "/home/uploader/Hello.world**

**python3 start.py -tracker partner -noup -f "/home/uploader/Hello.world**
***

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


 ![Install](https://img.shields.io/badge/How_to_Install-gr) 


1. Linux : sudo apt install ffmpeg
2. Windows : unzip https://www.ffmpeg.org/download.html and add its folder to
PATH environment user variable

3. Download the release zip
4. Unzip it
5. run pip install -r requirements.txt inside the bot folder
6. "python start.py" to initialize the configuration for the bot


#### Upload PDF
unit3dup can grab the first page, convert it to an image (using xpdf),
and then the bot can upload it to an image host, then add the link to the torrent page description

Install xpdf tools

Windows:

1. Download and unzip xpdfReader from https://dl.xpdfreader.com/xpdf-tools-win-4.05.zip
2. Put the folder 'bin64' in the system path. For example: C:\xpdf-tools-win-4.05\bin64
3. Test it: Run pdfimages.exe in the terminal

Linux:
1. sudo apt install xpdf
2. Test it: Run pdfimages in the terminal

### Configure
open the Unit3Dbot_service.json

-> Linux : Unit3Dbot.json is located in the home directory on Linux

-> Windows: Unit3Dbot.json is located in the AppData folder on Windows

example:

C:\Users\user\AppData\Local\Unit3Dup_config\
where "user" is your username windows account

## Bot Update
1. Delete only the bot folder
2. Download the release zip
3. Unzip it
4. finish 


| Trackers          | Description              |
|-------------------|--------------------------|
| `ITT`             | https://itatorrents.xyz/ |
| `SIS`             | https://shareisland.org/ |


## Join Us

The program is functional but still in the early stages, undergoing constant modifications.
You can help improve this project or just hang out with us on
[forum](https://itatorrents.xyz/forums/topics/414?page=1#post-1497)

[![Telegram](https://img.shields.io/badge/Telegram-contact-blue?style=for-the-badge&logo=telegram)](https://t.me/phantomdays)


Thank you

### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.
