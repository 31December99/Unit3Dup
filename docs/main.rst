Start.py
############

Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do


I Flags principali
********************

1. `-u` creates and uploads a `File`

2. `-f` creates and uploads a `Folder`

3. `-scan` creates and uploads every `Folder` **and** `Files`


Creare e caricare torrents
==============================

- If you want to create a torrent for a single file:


.. code-block:: python

    python start.py -u "C:\Archivio\The Movie 01.mkv"

- Single folder:

.. code-block:: python

    python start.py -f "C:\Archivio\The Movies"


- For one or more folders

.. code-block:: python

    python start.py -scan "C:\Archivio"


Create torrent but do not upload
==============================

Add the `-noup` flag

.. code-block:: python

    python start.py -noup -u "C:\Archive\The Movie 01.mkv"

- Single folder

.. code-block:: python

    python start.py -noup -f "C:\Archive\The Movies"

- For one or more folders

.. code-block:: python

    python start.py -noup -scan "C:\Archive"
