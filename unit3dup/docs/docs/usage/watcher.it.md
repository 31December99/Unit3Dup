# Watcher

Il watcher è la modalità **automatica**: il bot monitora una cartella e carica sul tracker tutto quello che ci arriva dentro. Utile in coppia con un client che scarica in una cartella fissa.

## Avvio

```bash
unit3dup -watcher
```

Il flag non accetta parametri: tutto si configura in `Unit3Dbot.json`.

## Configurazione

In `user_preferences` ([Opzioni avanzate](../config/options.md#watcher)):

```json
"WATCHER_INTERVAL": 60,
"WATCHER_PATH": "/percorso/cartella/sorgente",
"WATCHER_DESTINATION_PATH": "/percorso/cartella/destinazione",
```

- `WATCHER_PATH` → la cartella **monitorata** (es. dove vengono scaricati i file)
- `WATCHER_DESTINATION_PATH` → la cartella dove i file vengono **spostati** e da cui parte l'upload
- `WATCHER_INTERVAL` → ogni quanti **secondi** scatta il controllo

## Cosa fa a ogni ciclo

Allo scadere di `WATCHER_INTERVAL` (a schermo vedi il conto alla rovescia):

1. Controlla `WATCHER_PATH`; se è vuota, riparte il conto alla rovescia
2. **Sposta** tutti i file in `WATCHER_DESTINATION_PATH`, preservando le sottocartelle (le cartelle svuotate vengono rimosse)
3. Processa i file spostati e li **carica sul tracker** con seeding, come uno [`-scan`](upload.md)
4. Ricomincia

Il loop è infinito: si esce con ++ctrl+c++.

!!! warning "I file vengono spostati, non copiati"
    `WATCHER_PATH` viene **svuotata** a ogni ciclo. Non puntarla a una cartella i cui file devono restare dove sono (es. quella di seeding del client).

!!! tip "Cartella inesistente?"
    Se `WATCHER_PATH` non esiste o non è configurata, il bot si ferma con `Watcher path does not exist or is not configured`.
