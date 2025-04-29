Start.py
############

Always use **python start.py** when you want to send a command to the bot

- Open the console window and navigate to the bot folder

Flags
********************

- [-scan] If you want to create a torrent for a single file:

.. code-block:: python

    python start.py -u "C:\Archive\The Movie 01.mkv"

- [-f] Single folder:

.. code-block:: python

    python start.py -f "C:\Archive\The Movies"


- [-scan] For one or more folders

.. code-block:: python

    python start.py -scan "C:\Archive"


- [-noup] if you want to create torrent but do not upload

.. code-block:: python

    python start.py -noup -u "C:\Archive\The Movie 01.mkv"

- [-reseed] If you think you have the file for reseeding an old torrent with zero seeds (dead)

.. code-block:: python

    python start.py -reseed -u "C:\Archive\The Movie 01.mkv"
    python start.py -reseed -f "C:\Archive\The Movie 01"
    python start.py -reseed -scan "C:\Archive"

- [-force] If you want to set the category

.. code-block:: python

    python start.py -force movie -u "C:\Archive\Highlander.mkv"
    python start.py -force tv -u "C:\Archive\Highlander"
    python start.py -force game -u "C:\Archive\Highlander"
    python start.py -force edicola -u "C:\Archive\Highlander.pdf"


- [-noseed] if you don't want to seed the torrent after creating it

.. code-block:: python

    python start.py -noseed -u "C:\Archive\The Movie 01.mkv"
    python start.py -noseed -f "C:\Archive\The Movie 01"
    python start.py -noseed -scan "C:\Archive"