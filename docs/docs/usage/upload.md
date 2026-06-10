# Upload base

I tre flag fondamentali: `-u`, `-f`, `-scan`. Tutti portano a termine l'intero processo — analisi, screenshot, ricerca metadata, creazione `.torrent`, upload sul tracker, seeding nel client.

## `-u` — un singolo file

```bash
unit3dup -u "/home/ITT/upload/film.mkv"
```

Carica **un file**. Il bot lo analizza, ricava titolo e tag dal nome, crea il torrent.

## `-f` — una cartella

```bash
unit3dup -f "/home/ITT/upload/nomecartella"
```

Crea **un unico torrent con il contenuto della cartella**, che prende il nome della cartella. Dentro può esserci un film o una serie: per il bot non fa differenza.

Usalo per: stagioni complete, film in più parti, contenuti con file di accompagnamento.

## `-scan` — tutto il contenuto di un percorso

```bash
unit3dup -scan "/home/ITT/upload"
```

È `-u` e `-f` insieme: analizza **ogni file e ogni cartella** dentro il percorso (ricorsivamente) e processa tutto, un torrent per ogni elemento trovato.

!!! tip "Quanti contenuti alla volta?"
    Su cartelle molto grandi puoi limitare il numero di elementi processati con `FAST_LOAD` nelle [Opzioni avanzate](../config/options.md).

## Modificatori

Si combinano con `-u`, `-f` e `-scan`:

| Flag | Effetto |
|---|---|
| `-noup` | Crea solo il `.torrent` (nell'[archivio](../config/options.md#percorsi)), **niente upload** né seeding |
| `-noseed` | Upload sul tracker **senza seeding**: il torrent non viene consegnato al client |
| `-dup` | Controlla i [duplicati](../config/options.md#duplicati) sul tracker prima di caricare |
| `-personal` | Marca l'upload come **personal release** |
| `-force <categoria>` | Forza la categoria: `movie`, `tv`, `game`, `edicola` (senza argomento: `movie`) |
| `-notitle "<titolo>"` | Usa questo titolo per la ricerca su TMDB invece di quello ricavato dal nome del file |
| `-b` | Ricostruisce titolo e tag ([Tag e titoli](tags.md)) |
| `-tracker <NOME>` / `-mt` | Tracker di destinazione ([Multi-tracker](multitracker.md)) |
| `-reseed` | Modalità reseed ([Reseed](reseed.md)) |

## Esempio completo

```bash
unit3dup -mt -b -u "/home/parzival/TEST/scan/007 - Vivi e lascia morire (1973).mkv"
```

Analizza il file, ricostruisce titolo e tag, lo carica su **tutti** i tracker configurati e avvia il seeding.

!!! note "Cosa vedi a schermo"
    Il bot mostra una tabella dei file in lavorazione, poi per ogni contenuto: ricerca TMDB, estrazione screenshot, upload immagini, creazione torrent, risposta del tracker, invio al client. La guida [Primo upload passo-passo](../guides/primo-upload.md) descrive ogni fase.
