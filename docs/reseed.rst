Reseed
############

Utilizza sempre **python start.py** quando vuoi inviare un comando al bot

- Apri la finestra nera della console e accedi alla cartella del bot
- Il bot può ricevere da te uno o più comandi (**flag**) dipende cosa vuoi fare

Flag reseed
********************

`-reseed` Cerca fra i tuoi contenuti e li confronta con quelli del tracker


Come fare il reseed
==============================

- Se pensi di avere il file per il reseed di un vecchio torrent con seed pari a zero (dead)

.. code-block:: python

    python start.py -reseed -u "C:\Archivio\The Movie 01.mkv"

- Per una singola cartella

.. code-block:: python

    python start.py -reseed -f "C:\Archivio\The Movies"


- Per una una o più cartelle

.. code-block:: python

    python start.py -reseed -scan "C:\Archivio"