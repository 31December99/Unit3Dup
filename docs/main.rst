Start.py
############

Always use **python start.py** when you want to send a command to the Unit3Dup

- Open the console window and navigate to the Unit3Dup folder

Create and load
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


Search
********************


- [-s] if you want to perform a search using a word

.. code-block:: python

    python start.py -s Oblivion

- [-tmdb] if you want to perform a search using the TMDB ID

.. code-block:: python

    python start.py -tmdb 8009
    python start.py -imdb ...
    python start.py -mal ...
    python start.py -tvdb ...

    or IMDB MAL TVDB

- [-res] if you want to perform a search using Resolution

.. code-block:: python

    python start.py -res 1080p

- [-tmdb -res] if you want to perform a search using TMDB ID and Resolution

.. code-block:: python

    python start.py -tmdb 8009 -res 1080p

- [-up] if you want to perform a search using the username

.. code-block:: python

    python start.py -up Joi


- [-st] if you want to perform a search from the a specific start.date

.. code-block:: python

    python start.py -st 1999


- [-en]  if you want to perform a search up to a specific end.date

.. code-block:: python

    python start.py -en 1999


- [-file]  if you want to perform a search using the filename

.. code-block:: python

    python start.py -file "F.s. 1080p H265 Ita Ac3 Eng DTS 5.1 Eng.mkv"

- [-type]  if you want to perform a search using Type

.. code-block:: python

    python start.py -type remux



working in progress.... :)