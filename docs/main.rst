Start.py
############

Utilizza sempre **python start.py** quando vuoi inviare un comando al bot

- Apri la finestra nera della console e accedi alla cartella del bot
- Il bot può ricevere da te uno o più comandi (**flag**) dipende cosa vuoi fare

I Flags principali
********************

1. `-u` crea e carica un `File`

2. `-f` crea e carica una `Cartella`

3. `-scan` crea e carica ogni `Cartella` **e** `Files`


Creare e caricare torrents
==============================

- Se desideri creare un torrent per un singolo file, puoi farlo utilizzando il seguente comando:

.. code-block:: python

    python start.py -u "C:\Archivio\The Movie 01.mkv"

- Per una singola cartella

.. code-block:: python

    python start.py -f "C:\Archivio\The Movies"


- Per una una o pià cartelle

.. code-block:: python

    python start.py -scan "C:\Archivio"


Creare torrent ma non caricare
==============================

aggiungi il flag `-noup`

.. code-block:: python

    python start.py -noup -u "C:\Archivio\The Movie 01.mkv"

- Per una singola cartella

.. code-block:: python

    python start.py -noup -f "C:\Archivio\The Movies"


- Per una una o più cartelle

.. code-block:: python

    python start.py -noup -scan "C:\Archivio"


