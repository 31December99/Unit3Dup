# FTP

Con `-ftp` il bot si collega a un server FTP remoto, ti fa **navigare e scegliere i file** da un menu interattivo, li scarica in locale e li carica sul tracker.

## Configurazione

Sezione `options` di `Unit3Dbot.json`:

```json
"options": {
    "FTPX_USER": "user",
    "FTPX_PASS": "pass",
    "FTPX_IP": "127.0.0.1",
    "FTPX_PORT": 2121,
    "FTPX_LOCAL_PATH": "/percorso/download/locale",
    "FTPX_ROOT": ".",
    "FTPX_KEEP_ALIVE": "False"
}
```

| Chiave | Significato |
|---|---|
| `FTPX_USER` / `FTPX_PASS` | Credenziali del server FTP |
| `FTPX_IP` / `FTPX_PORT` | Indirizzo e porta del server |
| `FTPX_LOCAL_PATH` | Cartella locale dove scaricare i file |
| `FTPX_ROOT` | Cartella remota di partenza |
| `FTPX_KEEP_ALIVE` | Mantiene viva la connessione |

## Uso

```bash
unit3dup -ftp
```

1. Il bot si connette e mostra il contenuto della cartella remota in una **tabella numerata**
2. Navighi: selezioni una cartella per entrarci, un file per scaricarlo
3. `0` per uscire
4. Alla chiusura, se hai scaricato qualcosa: eventuali archivi **`.rar` vengono estratti** automaticamente, poi parte l'upload del contenuto scaricato (come [`-f`](upload.md))

!!! tip "Seedbox remota"
    Tipico uso: peschi le release dalla seedbox via FTP e le carichi sul tracker dalla macchina di casa, senza passaggi manuali.
