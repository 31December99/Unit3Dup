
Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do


Flag watcher
********************

`-watcher` it reads the contents of a folder and moves them to another destination folder, then uploads everything to the tracker

How to use watcher
==============================

The flag does not accept parameters

.. code-block:: python

    python start.py -watcher

The default folders are:

watcher_path

watcher_destination_path

How to configure the watcher
==============================

Open the `Unit3D.json` file with a text editor and set the attribute:

WATCHER_INTERVAL

Every WATCHER_INTERVAL (seconds), it checks `watcher_path`, then moves everything to `watcher_destination_path`, and uploads it to the tracker


