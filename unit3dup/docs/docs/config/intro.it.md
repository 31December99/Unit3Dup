# Configurazione — primi passi

## Dove sta la configurazione

Al **primo avvio** il bot crea la cartella `Unit3Dup_config` con dentro il file di configurazione principale e i file di supporto:

| Sistema | Percorso |
|---|---|
| Windows | `%LOCALAPPDATA%\Unit3Dup_config\` |
| Linux / macOS | `~/Unit3Dup_config/` |

Contenuto della cartella:

| File | A cosa serve |
|---|---|
| `Unit3Dbot.json` | **Configurazione principale**: tracker, api key, client torrent, preferenze |
| `tags_list.json` | Tag personalizzati per la costruzione dei titoli ([dettagli](../usage/tags.md)) |
| `sign_list.json` | Firme releaser ([dettagli](../usage/tags.md)) |
| `ban_list.json` | Tag da escludere dall'autobuild del titolo ([dettagli](../usage/tags.md)) |

!!! warning "Il file si chiama `Unit3Dbot.json`"
    In vecchie versioni della documentazione era indicato come "Unit3D.json": il nome corretto è **`Unit3Dbot.json`**.

Nella stessa cartella il bot crea anche le sottocartelle di default `torrent_archive_path` (dove archivia i `.torrent` generati), `cache_path`, `watcher_path` e `watcher_destination_path` — tutte personalizzabili (vedi [Opzioni avanzate](options.md)).

## La struttura del file

`Unit3Dbot.json` è diviso in **cinque sezioni**:

```json
{
    "tracker_config": { },
    "torrent_client_config": { },
    "user_preferences": { },
    "options": { },
    "console_options": { }
}
```

| Sezione | Contenuto | Pagina |
|---|---|---|
| `tracker_config` | URL e api key dei tracker, chiavi TMDB/TVDB/IGDB/YouTube, chiavi image host | [Tracker](trackers.md), [Metadata](metadata.md), [Image host](imagehosts.md) |
| `torrent_client_config` | qBittorrent, Transmission, rTorrent | [Client torrent](clients.md) |
| `user_preferences` | Screenshot, cache, watcher, duplicati, tag, lingua… | [Opzioni avanzate](options.md) |
| `options` | Connessione FTP | [FTP](../usage/ftp.md) |
| `console_options` | Colori e messaggi della console | [Opzioni avanzate](options.md) |

## Configurazione minima

Non serve compilare ogni riga. Per iniziare bastano:

1. **`ITT_URL` + `ITT_APIKEY`** (o il tuo tracker) — [Tracker](trackers.md)
2. **`TMDB_APIKEY`** — [Metadata](metadata.md)
3. **Almeno due chiavi image host** — [Image host](imagehosts.md)
4. **`TORRENT_CLIENT` + credenziali del client** — [Client torrent](clients.md)

I valori non configurati restano `no_key` / `no_pass` / `no_path`.

## Verifica la configurazione

```bash
unit3dup -check
```

Controlla i file di configurazione e l'ambiente. All'avvio il bot mostra sempre i percorsi attivi:

```text
[Configuration] '~/Unit3Dup_config/Unit3Dbot.json'
[*.torrent Archive] '~/Unit3Dup_config/torrent_archive_path'
[Images,Tmdb cache] '~/Unit3Dup_config/cache_path'
[Watcher] '~/Unit3Dup_config/watcher_path'
[Watcher] '~/Unit3Dup_config/watcher_destination_path'
[Preferred Language] 'all'
```

!!! danger "Errori bloccanti"
    Se un valore è malformato il bot esce subito con un messaggio tipo `-> Please Fix 'CAMPO' ['valore'] in settings.json`: apri `Unit3Dbot.json` e correggi il campo indicato.
