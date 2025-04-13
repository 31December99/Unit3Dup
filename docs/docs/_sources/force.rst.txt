
Utilizza sempre **python start.py** quando vuoi inviare un comando al bot

- Apri la finestra nera della console e accedi alla cartella del bot
- Il bot può ricevere da te uno o più comandi (**flag**) dipende cosa vuoi fare

Flag force
********************

`-force` Se vuoi impostare la categoria al posto del bot


Come utilizzare force
==============================

Aggiungi il flag il quale può essere combinato con -u, -f o -scan

.. code-block:: python

    python start.py -force movie -u "C:\Archivio\The Movie 01.mkv"

- Per una singola cartella

.. code-block:: python

    python start.py -force tv -f "C:\Archivio\The Movies"


- Per una una o più cartelle

.. code-block:: python

    python start.py -force game -scan "C:\Archivio"

.. code-block:: python

    python start.py -force edicola -u "C:\Archivio\The Manual"