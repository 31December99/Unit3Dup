Reseed
############

Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do


Flag reseed
********************

`-reseed` Searches through your contents and compares them with those on the tracker

How to perform reseed
==============================

- If you think you have the file for reseeding an old torrent with zero seeds (dead)

.. code-block:: python

    python start.py -reseed -u "C:\Archive\The Movie 01.mkv"

- Single folder

.. code-block:: python

    python start.py -reseed -f "C:\Archive\The Movies"

- For one or more folders

.. code-block:: python

    python start.py -reseed -scan "C:\Archive"
