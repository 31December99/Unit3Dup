# Multi-tracker

Il bot può caricare lo stesso contenuto su un tracker solo o su tutti quelli configurati in `MULTI_TRACKER` ([configurazione](../config/trackers.md)).

## `-tracker` — un tracker specifico

```bash
unit3dup -tracker ptt -u "/percorso/film.mkv"
```

Carica solo sul tracker indicato. Il nome deve essere presente nella lista `MULTI_TRACKER`, altrimenti:

```text
Tracker 'xyz' not found. Please update your configuration file
```

Senza `-tracker`, il bot usa il **primo tracker della lista** — vale anche per tutti i comandi di [ricerca](search.md).

## `-mt` — tutti i tracker

```bash
unit3dup -mt -u "/percorso/film.mkv"
```

Carica su **tutti** i tracker di `MULTI_TRACKER`, in sequenza: per ognuno crea il torrent con l'announce giusto, lo carica e lo mette in seeding.

All'avvio il bot verifica che ogni tracker risponda:

```text
Tracker -> 'ITT' Online
Tracker -> 'PTT' Online
```

!!! warning "Serve la PID di ogni tracker"
    Per ogni tracker in `MULTI_TRACKER` devono essere configurate `*_APIKEY` **e** `*_PID`: senza PID il bot esce con `-> No PID value`. Se non usi un tracker, toglilo dalla lista.
