# Tutti i comandi

Sinossi:

```text
unit3dup [opzioni]
```

I flag di upload si combinano tra loro (es. `-mt -b -u "<file>"`); i flag di ricerca si combinano con i filtri. Ogni flag esiste anche in forma lunga (`-u` / `--upload`).

## Configurazione

| Flag | Argomento | Descrizione |
|---|---|---|
| `-check` | — | Controlla i file di configurazione e l'ambiente |

## Upload

| Flag | Argomento | Descrizione |
|---|---|---|
| `-u`, `--upload` | percorso file | Carica un [singolo file](../usage/upload.md#-u-un-singolo-file) |
| `-f`, `--folder` | percorso cartella | Carica una [cartella](../usage/upload.md#-f-una-cartella) come unico torrent |
| `-scan` | percorso | Processa [tutto il contenuto](../usage/upload.md#-scan-tutto-il-contenuto-di-un-percorso) del percorso |
| `-b`, `--buildtags` | — | [Ricostruisce titolo e tag](../usage/tags.md#-b-ricostruisci-il-titolo) dall'analisi del media |
| `-reseed` | — | [Reseed](../usage/reseed.md): scarica dal tracker i torrent dei tuoi contenuti locali |
| `-watcher` | — | Avvia il [watcher](../usage/watcher.md) (cartella monitorata) |
| `-notitle` | "titolo" | [Titolo manuale](../usage/tags.md#titolo-manuale) per la ricerca TMDB |
| `-tracker` | nome tracker | [Tracker di destinazione](../usage/multitracker.md#-tracker-un-tracker-specifico) (default: il primo di `MULTI_TRACKER`) |
| `-mt` | — | Upload su [tutti i tracker](../usage/multitracker.md#-mt-tutti-i-tracker) configurati |
| `-force` | categoria | Forza la categoria: `movie`, `tv`, `game`, `edicola` (senza argomento: `movie`) |
| `-noseed` | — | Upload senza consegnare il torrent al client (niente seeding) |
| `-noup` | — | Crea solo il `.torrent` nell'archivio, niente upload |
| `-dup`, `--duplicate` | — | Controlla i duplicati sul tracker prima dell'upload |
| `-personal` | — | Marca come personal release |
| `-ftp` | — | [Browser FTP interattivo](../usage/ftp.md): scarica dal server remoto e carica |

## Ricerca

| Flag | Argomento | Descrizione |
|---|---|---|
| `-sch`, `--search` | "testo" | [Cerca](../usage/search.md) torrent per titolo |
| `-i`, `--info` | "testo" | Come `-sch` con informazioni dettagliate |
| `-dmp`, `--dump` | — | Dump completo dei titoli del tracker (salvato in locale) |
| `-db`, `--dbsave` | — | Salva i risultati della ricerca nel database locale |
| `-up`, `--uploader` | "nome" | Torrent di un uploader |
| `-d`, `--description` | "testo" | Cerca nelle descrizioni |
| `-bd`, `--bdinfo` | "testo" | Mostra il BDInfo dei risultati |
| `-m`, `--mediainfo` | "testo" | Mostra il MediaInfo dei risultati |

## Filtri

| Flag | Argomento | Descrizione |
|---|---|---|
| `-st`, `--startyear` | anno | Dall'anno in poi |
| `-en`, `--endyear` | anno | Fino all'anno |
| `-type` | tipo | Tipo di contenuto |
| `-res`, `--resolution` | risoluzione | Filtra per risoluzione |
| `-file`, `--filename` | "nome" | Filtra per nome file |
| `-se`, `--season` | numero | Stagione |
| `-ep`, `--episode` | numero | Episodio |
| `-tmdb` | ID | Per ID TMDB (con `-res`: combo titolo+risoluzione) |
| `-imdb` | ID | Per ID IMDB |
| `-tvdb` | ID | Per ID TVDB |
| `-mal` | ID | Per ID MyAnimeList |
| `-playid` | ID | Per playlist |
| `-coll` | ID | Per collection |
| `-free` | percentuale | Per percentuale freeleech |
| `-al`, `--alive` | — | Solo torrent vivi |
| `-dd`, `--dead` | — | Solo torrent morti |
| `-dy`, `--dying` | — | Solo torrent morenti |

## Viste speciali

| Flag | Descrizione |
|---|---|
| `-du`, `--doubleup` | Torrent DoubleUp |
| `-fe`, `--featured` | Torrent Featured |
| `-re`, `--refundable` | Torrent Refundable |
| `-str`, `--stream` | Torrent stream-friendly |
| `-sd`, `--standard` | Torrent SD |
| `-hs`, `--highspeed` | Torrent Highspeed |
| `-int`, `--internal` | Release Internal |
| `-pr`, `--prelease` | Personal release |
