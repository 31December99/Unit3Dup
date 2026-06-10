# Primo upload passo-passo

Da zero al primo torrent caricato su ITT. Tempo stimato: 15 minuti.

## 1. Installa

Segui la pagina per il tuo sistema: [Windows](../install/windows.md) · [Linux](../install/linux.md) · [Seedbox ultra.cc](../install/seedbox.md).

Poi lancia una volta il bot per fargli creare i file di configurazione:

```bash
unit3dup
```

I messaggi rossi sono attesi: il bot non è ancora configurato.

## 2. Configura il minimo indispensabile

Apri `Unit3Dbot.json` (Windows: `%LOCALAPPDATA%\Unit3Dup_config\` — Linux: `~/Unit3Dup_config/`) e compila questi campi:

```json
{
    "tracker_config": {
        "ITT_URL": "https://itatorrents.xyz",
        "ITT_APIKEY": "la_tua_api_key",
        "ITT_PID": "la_tua_passkey",
        "MULTI_TRACKER": ["itt"],
        "TMDB_APIKEY": "la_tua_chiave_tmdb",
        "IMGBB_KEY": "la_tua_chiave_imgbb",
        "FREE_IMAGE_KEY": "la_tua_chiave_freeimage"
    },
    "torrent_client_config": {
        "QBIT_USER": "admin",
        "QBIT_PASS": "la_tua_password",
        "QBIT_HOST": "127.0.0.1",
        "QBIT_PORT": "8080",
        "TORRENT_CLIENT": "qbittorrent"
    }
}
```

(Le altre sezioni e chiavi restano come sono.)

Dove trovare ogni valore:

- **API key e PID di ITT** → sul tracker, nelle impostazioni del tuo profilo ([dettagli](../config/trackers.md))
- **TMDB** → account gratuito su [themoviedb.org](https://www.themoviedb.org/) → Impostazioni → API ([dettagli](../config/metadata.md))
- **Image host** → registrati su [imgbb.com](https://imgbb.com) e [freeimage.host](https://freeimage.host), genera le chiavi ([dettagli](../config/imagehosts.md))
- **qBittorrent** → credenziali della WebUI ([dettagli](../config/clients.md))

!!! tip "MULTI_TRACKER ridotto"
    `"MULTI_TRACKER": ["itt"]` con solo il tuo tracker: eviti errori di PID per tracker che non usi.

## 3. Verifica

```bash
unit3dup -check
```

Se qualcosa non va, il bot ti dice quale campo correggere.

## 4. Primo upload

Scegli un file video di prova che rispetti le regole del tracker, poi:

```bash
unit3dup -u "/percorso/del/film.mkv"
```

Cosa succede, nell'ordine:

1. **Analisi** — il bot esamina il file e mostra la tabella dei contenuti in lavorazione
2. **Ricerca metadata** — interroga TMDB e ti propone l'ID del titolo
3. **Screenshot** — estrae le immagini dal video e le carica sull'image host
4. **Torrent** — genera il `.torrent` e lo salva nell'archivio (`torrent_archive_path/ITT/`)
5. **Upload** — invia tutto al tracker e riceve il link della pagina
6. **Seeding** — consegna il torrent a qBittorrent, che parte subito col seed

## 5. Controlla il risultato

- La pagina del torrent sul tracker: titolo, tag, screenshot, mediainfo
- qBittorrent: il torrent dev'essere in seeding con l'etichetta configurata in `TAG`

Se tutto torna: fatto. Prossimi passi: [Upload base](../usage/upload.md) per `-f` e `-scan`, [Tag e titoli](../usage/tags.md) per rifinire i titoli, [Multi-tracker](../usage/multitracker.md) per caricare ovunque.
