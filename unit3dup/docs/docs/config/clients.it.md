# Client torrent

Sezione `torrent_client_config` di `Unit3Dbot.json`. Dopo l'upload il bot consegna il torrent al tuo client per il **seeding**.

## Scegli il client

```json
"TORRENT_CLIENT": "qbittorrent",
```

Valori possibili: `qbittorrent`, `transmission`, `rtorrent`.

Il client è **obbligatorio** per qualsiasi operazione di upload con seeding (`-u`, `-f`, `-scan`, `-watcher`, `-reseed`): all'avvio il bot testa la connessione e, se fallisce o il nome non è valido, esce con `Unknown Torrent Client name` o errore di connessione.

!!! tip "Niente client?"
    Con `-noseed` (upload senza seeding) o `-noup` (crea solo il `.torrent`) il client non viene contattato.

## qBittorrent

```json
"QBIT_USER": "admin",
"QBIT_PASS": "la_tua_password",
"QBIT_HOST": "127.0.0.1",
"QBIT_PORT": "8080",
"SHARED_QBIT_PATH": "no_path",
```

Credenziali della **WebUI** (in qBittorrent: *Strumenti → Opzioni → WebUI*). `QBIT_HOST` accetta l'IP della macchina dove gira il client.

## Transmission

```json
"TRASM_USER": "admin",
"TRASM_PASS": "la_tua_password",
"TRASM_HOST": "127.0.0.1",
"TRASM_PORT": "9091",
"SHARED_TRASM_PATH": "no_path",
```

## rTorrent

```json
"RTORR_USER": "admin",
"RTORR_PASS": "la_tua_password",
"RTORR_HOST": "127.0.0.1",
"RTORR_PORT": "9091",
"SHARED_RTORR_PATH": "no_path",
```

## SHARED_*_PATH — client su un'altra macchina

Se il client torrent gira su una macchina, un container o un OS **diverso** da quello dove lanci il bot, i percorsi locali dei tuoi file non coincidono con quelli visti dal client.

`SHARED_*_PATH` è il percorso **come lo vede il client**: il bot lo usa al posto del percorso locale quando registra il torrent per il seeding.

Esempio — bot su Windows, qBittorrent in un container che monta la stessa cartella su `/downloads`:

```json
"SHARED_QBIT_PATH": "/downloads",
```

## TAG

```json
"TAG": "ADDED TORRENTS",
```

Etichetta/categoria applicata ai torrent aggiunti dal bot nel client: utile per riconoscerli e filtrarli.
