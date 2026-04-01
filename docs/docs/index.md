# Benvenuto in Unit3dUp Docs 0.9.20

Unit3Dup è uno programma in python per creare e caricare su tracker i vostri torrents.

Il workflow è il seguente:

- User fornisce un percorso di una cartella o di un file
- Bot analizza il file o i files e autonomamente crea per ognuno un oggetto
- Ogni oggetto ha diverse proprietà
- Le proprietà descrivono l'oggetto che verrà caricato sul tracker insieme al torrent

## Il percorso

unit3dup è il nome del bot e del file eseguibile. Il bot viene quindi lanciato da linea di comando con varie opzioni
solo quelle basi sono obbligatorie. Le opzioni sono chiamate flag.

### Flag di base

Questi sono i flag di base per creare uno o più torrents e caricarli sul tracker
Esistono anche altri flag non obbligatori non qui descritti

**-u: unico file**

Crea e carica un torrent

```unit3dup -u "/home/ITT/upload/....mkv"```


**-f: Il bot tiene conto del nome del folder**

La cartella può contenere un movie o una serie
Per il bot non fa differenza. Soltanto un file viene analizzato per mediainfo

Crea e carica quindi un torrent con il contenuto del folder

```unit3dup -f "/home/ITT/upload/nomecartella"```

**-scan: Il bot crea un elenco di files e sottocartelle e per ogni file si comporterà
come per il flag '-u' mentre per ogni folder come il flag '-f'**

```unit3dup -scan "/home/ITT/upload/nomecartella"```


## L'oggetto..

Esistono tre tipi di oggetto

- Oggetto video
- Oggetto Documenti
- Oggetto Game

### Oggetto Video

Il bot crea un **oggetto video** per ogni file video che incontra, con le proprietà che seguono:

- `name` : **Nome del torrent** e nome visualizzato sulla pagina del tracker
- `tmdb` : ID del video ottenuto interrogando il database online **TheMovieDatabase** 
- `tvdb` : ID del video ottenuto interrogando il database online **TheTVDB**
- `imdb` : ID del video ottenuto dal risultato di TVDB
- `keywords` : Keywords ottenute dal risultato di TMDB
- `category_id`: ID del tracker che identifica il tipo di video **Movie** o **Serie**
- `resolution_id`: ID del tracker che identifica la risoluzione 
- `sd` : ID del tracker che identifica se un video è almeno HD o SD
- `anonymous` : Se settato previene la lettura dell'username
- `mediainfo` : L'output di mediainfo che contiene le informazioni tecniche del video
- `description` : lo spazio dove vengono inseriti gli url degli **screenshot e descrizione** personale 
- `type_id` : ID del tracker che identifica la sorgente
- `season_number` : numero di stagione
- `episode_number` : numero di episodio oppure 0 quando è un **torrent pack**
- `personal_release` : indica che questa è una **personal release**
 
### Oggetto Documenti

L'oggetto ```documenti``` ha sicuramente meno proprietà in comune con il video.
Fanno eccezione `tmdb` e `resolution_id` perché ritenuti campi obbligatori dal tracker
e settati come valori neutrali

- `name`
- `tmdb`
- `category_id`
- `anonymous`
- `description`
- `type_id`
- `resolution_id`
- `personal_release`

La descrizione di ogni proprietà è la stessa del video

### Oggetto Game

Lo stesso vale per `Game` con tmdb settato come valore neutrale.
Si aggiunge inoltre la proprietà `igdb`, per la quale è necessario avere un account IGDB.

IGDB fornisce un ID del suo database online come per tmdb e tvdb

- `name`
- `tmdb`
- `category_id`
- `anonymous`
- `description`
- `type_id`
- `igdb`
- `personal_release`

