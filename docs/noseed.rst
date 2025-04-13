
Utilizza sempre **python start.py** quando vuoi inviare un comando al bot

- Apri la finestra nera della console e accedi alla cartella del bot
- Il bot può ricevere da te uno o più comandi (**flag**) dipende cosa vuoi fare

Flag noseed
********************

`-noseed` Crea e carica il torrent ma non lo invia al client torrent


Come utilizzare noseed
==============================

Il flag non accetta parametri

.. code-block:: python

    python start.py -nseed -u "C:\Archivio\The Movie 01.mkv"

- Per una singola cartella

.. code-block:: python

    python start.py -noseed -f "C:\Archivio\The Movies"


- Per una una o più cartelle

.. code-block:: python

    python start.py -noseed -scan "C:\Archivio"


