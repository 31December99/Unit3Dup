# Unit3D_uploader
Unit3D platform uploader

# Torrent Generator and Uploader

The program is functional but still in an early stage, undergoing constant modifications.

This Python script generates and uploads torrents based on input provided for movies or TV series. It performs the following tasks:

- Compiles various metadata information to create a torrent.
- Extracts a series of screenshots directly from the video.
- Generates meta-info derived from the video.
- Searches for the corresponding ID on TMDB (The Movie Database).
- Uploads the content to the UNIT3D Next Generation tracker platform.
- Seeding in qbittorrent

## Usage

1. Provide a Movie or TV Series title as input.
2. Run the Python script.
3. The script will create a torrent, extract screenshots, generate meta-information, search for TMDB ID, and upload to UNIT3D.

## Dependencies

- requiremensts.txt
- python -m spacy download it_core_news_md
## Installation

1. Clone this repository.
2. Install the required dependencies using PIP.
3. Make sure to run the script followed by the command "-movie" and the path to the file or "-serie" followed
   by the folder containing the series.
4. Config address and port for qbittorent webui
5. Run the script with botITT.py

## Configuration

Make sure to configure the necessary API keys and authentication credentials in a separate configuration file (.env).

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License

# .env file Example:

- ITT_BASE_URL=https://itatorrents.xyz/
- ITT_PASS_KEY=xxxxxxxx
- ITT_API_TOKEN=xxxxxx
- TMDB_APIKEY=xxxxx
- IMGBB_KEY=xxxxxx
- QBIT_USER=xxxxxxx
- QBIT_PASS=xxxxxx
- QBIT_PORT=xxxxxx
- 
# ITT_BASE_URL
Tracker URL

# ITT_PASS_KEY
Your tracker pass key ( Search for it in your user profile)

# ITT_API_TOKEN
As mentioned above

# TMDB_APIKEY
Your TMDB Api key ( Search for it in your user profile)

# IMGBB_KEY
Your IMGBB Api key ( Search for it in your user profile)

# QBIT_USER
Qbittorrent USER

# QBIT_PASS
Qbittorrent PASS
