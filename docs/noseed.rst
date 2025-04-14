Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do


Flag noseed
********************

`-noseed` Creates and uploads the torrent but does not send it to the torrent client

How to use noseed
==============================

The flag does not accept parameters

.. code-block:: python

    python start.py -noseed -u "C:\Archive\The Movie 01.mkv"

- Single folder

.. code-block:: python

    python start.py -noseed -f "C:\Archive\The Movies"

- For one or more folders

.. code-block:: python

    python start.py -noseed -scan "C:\Archive"
