# Tag e titoli

Il titolo del torrent è composto dal **titolo del media** più una serie di **tag** ricavati dall'analisi del file: risoluzione, sorgente, codec audio/video, lingua, HDR…

Tag generabili: `version`, `resolution`, `uhd`, `platform`, `source`, `remux`, `multi`, `acodec`, `channels`, `flag`, `subtitle`, `vcodec`, `hdr`, `video_encoder`.

## `-b` — ricostruisci il titolo

```bash
unit3dup -b -u "/percorso/film.mkv"
```

Con `-b/--buildtags` il bot **ricostruisce da zero** titolo e tag a partire dall'analisi tecnica del media (MediaInfo) e dal nome del file, nell'ordine definito da `TAGS_POSITION_MOVIE` / `TAGS_POSITION_SERIE` ([Opzioni avanzate](../config/options.md#posizione-dei-tag-nel-titolo)).

Senza `-b`, il titolo resta più fedele al nome originale del file.

## I tre file di personalizzazione

Stanno nella cartella di configurazione (`Unit3Dup_config`) e vengono creati al primo avvio con valori di default. Sono JSON modificabili con un editor di testo.

### `tags_list.json` — tag personalizzati

Mappa **parola → tipo di tag**: insegna al bot a riconoscere parole nei nomi dei file e classificarle.

```json
{
    "REMUX": "remux",
    "WEB-DL": "source",
    "AMZN": "platform"
}
```

Usato da `-b`: se nel nome del file compare la parola, il valore corrispondente finisce nel tag giusto del titolo. Puoi aggiungere le tue voci (es. sigle di release group o sorgenti particolari).

!!! warning "File richiesto da `-b`"
    Se `tags_list.json` manca, il bot lo segnala all'avvio quando usi `-b`.

### `ban_list.json` — parole da eliminare

Lista di parole **rimosse dal titolo** durante la ricostruzione: roba che non deve finire sulla pagina del tracker (sigle di siti, spazzatura nei nomi dei file…).

### `sign_list.json` — firme releaser

Lista delle firme riconosciute come **release group**. Insieme a `RELEASER_SIGN` ([Opzioni avanzate](../config/options.md#lingua-anonimato-e-firma)) gestisce la firma in coda al titolo (max 20 caratteri, caratteri speciali rimossi).

## Titolo manuale

Quando il nome del file è troppo sporco per ricavarne il titolo (capita con i pack di stagioni senza titolo):

```bash
unit3dup -u "/percorso/S01.pack.1080p.mkv" -notitle "Nome Della Serie"
```

`-notitle` forza il titolo usato per la **ricerca su TMDB**, senza toccare i tag tecnici.
