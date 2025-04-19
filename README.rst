
**Hello !**
===============================================
|version| |online| |status| |python| |ubuntu| |debian| |windows|

.. |version| image:: https://img.shields.io/badge/Unit3Dup-0.7.11-blue
.. |online| image:: https://img.shields.io/badge/Online-green
.. |status| image:: https://img.shields.io/badge/Status-Active-brightgreen
.. |python| image:: https://img.shields.io/badge/Python-3.10+-blue
.. |ubuntu| image:: https://img.shields.io/badge/Ubuntu-22-blue
.. |debian| image:: https://img.shields.io/badge/Debian-12-blue
.. |windows| image:: https://img.shields.io/badge/Windows-10-blue

Auto Torrent Generator and Uploader
===================================

This Python script generates and uploads torrents based on input provided for movies or TV series and Games.

It performs the following tasks:

- Scan folder and subfolders
- Compiles various metadata information to create a torrent
- Extracts a series of screenshots directly from the video
- Add webp to your torrent description page
- Extracts cover from the PDF documents
- Generates meta-info derived from the video or game
- Searches for the corresponding ID on TMDB, IGDB or IMDB
- Add trailer from TMDB or YouTube
- Seeding in qBittorrent, Transmission or rTorrent
- Reseeding one or more torrents at a time
- Seed your torrents across different OS
- Add a custom title to your seasons
- Generate info for a title using MediaInfo

.. image:: https://img.shields.io/badge/Upload_PDF-gr
   :alt: Install Upload PDF

unit3dup can grab the first page, convert it to an image (using xpdf),
and then the bot can upload it to an image host, then add the link to the torrent page description.

.. image:: https://img.shields.io/badge/WINDOWS-Install_poppler_tools-gr
   :alt: Windows Poppler Tools

WINDOWS Installation
--------------------

1. Download and unzip poppler for Windows from https://github.com/oschwartz10612/poppler-windows/releases
2. Unzip it
3. Put the folder 'bin' in the system path (e.g. ``C:\poppler-24.08.0\Library\bin``)
4. *Close and reopen a new console window*
5. Test it: Run ``pdftocairo`` in the terminal

.. image:: https://img.shields.io/badge/LINUX-Install_poppler_tools-gr
   :alt: Linux Poppler Tools

LINUX Installation
------------------

1. Run: ``sudo apt install poppler-utils``
2. Test it: Run ``pdftocairo`` in the terminal


.. image:: https://img.shields.io/badge/Bot_UPDATE-gr
   :alt: Bot Update

Bot Update
----------

1. Delete only the bot folder
2. Download the release zip
3. Unzip it
4. No config needed
5. Done!

Join Us
----------

`Telegram <https://t.me/+hj294GabGWJlMDI8>`_
`Forum <https://itatorrents.xyz/forums/topics/414?page=1#post-2160>`_
