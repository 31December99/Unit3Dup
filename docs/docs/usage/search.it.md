# Ricerca sul tracker

Oltre a caricare, il bot interroga il tracker dal terminale: ricerche, dettagli, filtri. Tutti i comandi operano sul **tracker di default** (il primo di `MULTI_TRACKER`) oppure su quello indicato con `-tracker <NOME>`.

## Ricerche di base

| Comando | Cosa fa |
|---|---|
| `-sch "<testo>"` | Cerca torrent per titolo |
| `-i "<testo>"` | Come `-sch` ma mostra le **informazioni dettagliate** di ogni risultato |
| `-dmp` | **Dump completo** di tutti i titoli del tracker (salvato in locale) |
| `-up "<uploader>"` | Torrent di un certo uploader |
| `-d "<testo>"` | Cerca nel testo delle **descrizioni** |
| `-bd "<testo>"` | Mostra il **BDInfo** dei torrent trovati |
| `-m "<testo>"` | Mostra il **MediaInfo** dei torrent trovati |
| `-db` | Aggiunto a una ricerca, **salva i risultati** nel database locale |

```bash
unit3dup -sch "nome del film"
unit3dup -tracker ptt -sch "nome del film"
unit3dup -up "NomeUploader" -db
```

## Filtri

| Filtro | Significato |
|---|---|
| `-st <anno>` / `-en <anno>` | Dall'anno / fino all'anno |
| `-type <tipo>` | Tipo di contenuto |
| `-res <risoluzione>` | Risoluzione |
| `-file "<nome>"` | Nome file |
| `-se <n>` / `-ep <n>` | Stagione / episodio |
| `-tmdb <id>` `-imdb <id>` `-tvdb <id>` `-mal <id>` | Per ID database esterni |
| `-playid <id>` / `-coll <id>` | Playlist / collection |
| `-free <valore>` | Percentuale freeleech |
| `-al` / `-dd` / `-dy` | Stato: vivi / morti / morenti |

Combo utile — un titolo TMDB a una risoluzione precisa:

```bash
unit3dup -tmdb 603 -res 1080p
```

## Viste speciali

Elenchi per attributo del torrent:

| Flag | Mostra |
|---|---|
| `-du` | DoubleUp |
| `-fe` | Featured |
| `-re` | Refundable |
| `-str` | Stream-friendly |
| `-sd` | Standard definition |
| `-hs` | Highspeed |
| `-int` | Internal |
| `-pr` | Personal release |

```bash
unit3dup -fe
```

La tabella completa di ogni flag: [Tutti i comandi](../reference/commands.md).
