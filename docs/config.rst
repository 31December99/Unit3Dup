Configuration file
##################

The file config is a json file created the first time you run the Unit3Dup

it's named Unit3Dup.json

Windows
*******

The file is created in
.. code-block:: python

    C:\\Users\\[USER]\\AppData\\Local\\Unit3Dup_config

Debian/Ubuntu
*************

The file is created in
.. code-block:: python

    /home/[user]




Settings Overview
*****************

MINIMAL
=======

.. code-block:: python

        ITT_URL:        Tracker URL
        ITT_APIKEY:     Trackr APIKEY
        ITT_PID:        Tracker PASSKEY
        TMDB_APIKEY:    The Movie DB APIKEY


At least one:

.. code-block:: python

        IMGBB_KEY:      Host APIKEY
        FREE_IMAGE_KEY: Host APIKEY
        LENSDUMP_KEY:   Host APIKEY
        PTSCREENS_KEY:  Host APIKEY
        IMGFI_KEY:      Host APIKEY


At least one client

.. code-block:: python

        QBIT_USER: admin
        QBIT_PASS: password
        QBIT_HOST: 127.0.0.1
        QBIT_PORT: 8080

        TRASM_USER: admin
        TRASM_PASS: password
        TRASM_HOST: 127.0.0.1
        TRASM_PORT: 9091

        RTORR_HOST: 192.168.1.41
        RTORR_PASS: password
        RTORR_PORT: 5000
        RTORR_USER: admin

        TORRENT_CLIENT: qbittorrent or Transmission or rTorrent



Preferences
===========

Game ID and media

.. code-block:: python

   IGDB_CLIENT_ID: Client ID used to fetch game media from the IGDB database.
   IGDB_ID_SECRET: Secret ID


Torrent Clients

.. code-block:: python

   SHARED_QBIT_PATH: Set this if you're running the bot on Linux but seeding with qBittorrent on Windows
                     or viceversa
   SHARED_RTORR_PATH: Like above but for rTorrent
   TORRENT_ARCHIVE_PATH: Set the path for the torrent file created by the bot
   TORRENT_COMMENT: Add a comment to your torrent file

Trailers

.. code-block:: python

   YOUTUBE_KEY: YouTube API key used to fetch a trailer if TMDb does not provide one
   YOUTUBE_FAV_CHANNEL_ID: When enabled, forces the bot to search trailers only within this YouTube channel instead of using a global search
   YOUTUBE_CHANNEL_ENABLE: Enable youtube channel

Duplicate

.. code-block:: python

   DUPLICATE_ON: Search for a title, check the release year, size, and episode information for duplicates
   SKIP_DUPLICATE: Automatically skip upload if a duplicate is found
   SIZE_TH: Set the acceptable size delta between your title and the one present on the tracker
   SKIP_TMDB: Automatically skip if no TMDb ID is found for the title


Screenshots
Host image priority. Tries the next one if the current fails (1:5). 1 = highest priority

.. code-block:: python

   NUMBER_OF_SCREENSHOTS: 3
   PTSCREENS_PRIORITY: 2
   LENSDUMP_PRIORITY: 3
   FREE_IMAGE_PRIORITY: 1
   IMGBB_PRIORITY: 4
   IMGFI_PRIORITY: 5
   COMPRESS_SCSHOT: Compression level for screenshots (0:9) 9 = max
   RESIZE_SCSHOT: Enable screenshot resizing while preserving aspect ratio


General

.. code-block:: python

   PREFERRED_LANG:  Choose your preferred language (eg ITA-ENG) Skip if the video does not match your selected language
   ANON: Anonymity
   PERSONAL_RELEASE: Set the flag personal release
   WEBP_ENABLED: In addition to the screenshot create an animated one

Cache

.. code-block:: python

   CACHE_SCR: Activate cache for the screenshots
   CACHE_PATH: Set the main path for storing cache files
   CACHE_DBONLINE: Activate cache for the TMBD o IMDB search