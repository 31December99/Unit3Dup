
**Hi !**
===============================================
|version| |online| |status| |python| |ubuntu| |debian| |windows|

.. |version| image:: https://img.shields.io/pypi/v/unit3dup.svg
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
- Searches for the corresponding ID on TMDB, IGDB, IMDB,TVDB
- Add trailer from TMDB or YouTube
- Seeding in qBittorrent, Transmission or rTorrent
- Reseeding one or more torrents at a time
- Seed your torrents across different OS
- Generate various tags for titles: ``version``, ``resolution``, ``uhd``, ``platform``, ``source``, ``remux``, ``multi``, ``acodec``, ``channels``, ``flag``, ``subtitle``, ``vcodec``, ``hdr``, ``video_encoder``


unit3dup can grab the first page, convert it to an image (using xpdf),
and then the bot can upload it to an image host, then add the link to the torrent page description.


Install and Upgrade
===================

- pip install unit3dup --upgrade

Windows Dependencies
--------------------
1. Download and unzip https://www.ffmpeg.org/download.html and add its folder to
   PATH environment user variable


Only for pdf
~~~~~~~~~~~~
1. Download and unzip poppler for Windows from https://github.com/oschwartz10612/poppler-windows/releases
2. Put the folder 'bin' in the system path (e.g. ``C:\poppler-24.08.0\Library\bin``)
3. *Close and reopen a new console window*
4. Test it: Run ``pdftocairo`` in the terminal


Ubuntu/Debian Dependencies
--------------------------
- sudo apt install ffmpeg

Only for pdf
~~~~~~~~~~~~
- sudo apt install poppler-utils


RUN
======

.. code-block:: python

   unit3dup -u <filepath>
   unit3dup -f <folderpath>
   unit3dup -scan <folderpath>



DOC
===

Commands list `Unit3Dup <https://31december99.github.io/Unit3Dup/commands/>`_


ImageHost
=========

The bot can upload images to the following image hosting platforms:

+------------------+----------------------------+
| **Image Host**   | **URL**                    |
+==================+============================+
| ``ImgBB``        | https://imgbb.com          |
+------------------+----------------------------+
| ``FreeImage``    | https://freeimage.host     |
+------------------+----------------------------+
| ``PtScreens``    | https://ptscreens.com      |
+------------------+----------------------------+
| ``LensDump``     | https://lensdump.com       |
+------------------+----------------------------+
| ``ImgFI``        | https://imgfi.com          |
+------------------+----------------------------+
| ``PassIMA``      | https://passtheima.ge      |
+------------------+----------------------------+
| ``ImaRide``      | https://www.imageride.net  |
+------------------+----------------------------+

Trackers
========

The Italian tracker: a multitude of people from diverse technical and social backgrounds,
united by a shared passion for torrents and more

+------------------+----------------------------+
| **Trackers**     | **Description**            |
+==================+============================+
| ``ITT``          | https://itatorrents.xyz    |
|                  |                            |
| ``PTT``          | https://polishtorrent.top  |
|                  |                            |
| ``AST``          | https://arabicsource.net   |
+------------------+----------------------------+

.. image:: https://img.shields.io/discord/1214696147600408698?label=Discord&logo=discord&style=flat
   :target: https://discord.gg/8RpwN2Khcz
   :alt: Discord Server


# AstraeLabs
======================

 `GitHub Project <https://github.com/AstraeLabs/VibraVid>`_

An open-source script for downloading movies, TV shows, and anime from various websites,
built by a community of people with a shared interest in programming.

.. image:: https://img.shields.io/badge/AstraeLabs-blue.svg
   :target: https://github.com/AstraeLabs/VibraVid
   :alt: AstraeLabs Badge

