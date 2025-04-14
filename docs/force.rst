
Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do

Flag force
********************

`-force` If you want to set the category instead of the bot


How to use force
==========================

Add the flag, which can be combined with -u, -f, or -scan

- Single file:

.. code-block:: python

    python start.py -force movie -u "C:\Archivio\The Movie 01.mkv"

- Single folder

.. code-block:: python

    python start.py -force tv -f "C:\Archivio\The Movies"


- For one or more folders:

.. code-block:: python

    python start.py -force game -scan "C:\Archivio"

.. code-block:: python

    python start.py -force edicola -u "C:\Archivio\The Manual"