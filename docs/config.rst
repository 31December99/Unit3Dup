Configuration file
##################

The file config is a json file created the first time you run the Uit3Dup

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

.. code-block:: python

   YOUTUBE_KEY": YouTube APIKEY
   IGDB_CLIENT_ID: IGDB(TWICH) CLIENT_ID
   IGDB_ID_SECRET: IGDB(TWICH) SECRET_ID

   SHARED_QBIT_PATH: TWO OS shared the same folder
   SHARED_RTORR_PATH: TWO OS shared the same folder


Host image priority. Tries the next one if the current fails. 1 = highest priority

.. code-block:: python

   PTSCREENS_PRIORITY: 2
   LENSDUMP_PRIORITY: 3
   FREE_IMAGE_PRIORITY: 1
   IMGBB_PRIORITY: 4
   IMGFI_PRIORITY: 5

