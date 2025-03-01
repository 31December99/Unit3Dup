## Unit3D_uploader
Unit3D platform uploader (Python >=3.10)

## Auto Torrent Generator and Uploader

This Python script generates and uploads torrents based on input provided for movies or TV series and Games.

It performs the following tasks:

- Scan subfolders
- Compiles various metadata information to create a torrent.
- Extracts a series of screenshots directly from the video.
- Generates meta-info derived from the video or Game.
- Searches for the corresponding ID on TMDB and IGDB.
- Add trailer from Tmdb or Youtube
- Uploads the content to the UNIT3D Next Generation tracker platform.
- Seeding in qbittorrent or transmission

___

### Upload single episode or movie '-u' command
This command allows you to create and upload torrent for movies and series
and automatically upload and seed them.

Example:
python3 start.py -u "/home/uploader/myvideos/S04E12.mkv

### Upload single folder '-f' command

Example:
python3 start.py -f "/home/uploader/seriedummy S01"

### Upload movies, series, and games with a single command

- `python3 start.py -scan "/home/uploader/archive


### How to Install 

1. Linux : sudo apt install ffmpeg
2. Windows : unzip https://www.ffmpeg.org/download.html and add its folder to
PATH environment user variable

3. Download the release zip
4. Unzip it
5. run pip install -r requirements.txt inside the bot folder
6. "python start.py" to initialize the configuration for the bot

### Configure
open the Unit3Dbot_service.json

-> Linux : Unit3Dbot_service.json is located in the home directory on Linux

-> Windows: Unit3Dbot_service.json is located in the AppData folder on Windows

example:

C:\Users\user\AppData\Local
where "user" is your username windows account

## Bot Update
1. Delete only the bot folder
2. Download the release zip
3. Unzip it
4. finish 

## Join Us

The program is functional but still in the early stages, undergoing constant modifications.
You can help improve this project or just hang out with us on
[forum](https://itatorrents.xyz/forums/topics/414?page=1#post-1497) 

Thank you

### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.
