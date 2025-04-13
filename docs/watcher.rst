
Utilizza sempre **python start.py** quando vuoi inviare un comando al bot

- Apri la finestra nera della console e accedi alla cartella del bot
- Il bot può ricevere da te uno o più comandi (**flag**) dipende cosa vuoi fare

Flag watcher
********************

`-watcher` Ogni 60 secondi legge il contenuto di una cartella e lo sposta in un'altra cartella
di destinazione. Quindi carica tutto sul tracker


Come utilizzare watcher
==============================

Il flag non accetta parametri

.. code-block:: python

    python start.py -watcher


Le cartelle di default sono

watcher_path

watcher_destination_path

Ogni 60 secondi verifica `watcher_path` allo scadere sposta tutto in `watcher_destination_path`
quindi carica sul tracker


Come configurare il watcher
==============================

Aprire con un editor di testo Unit3D.json e settare con un valore in secondi l'attributo:

WATCHER_INTERVAL

Default è 60 secondi
