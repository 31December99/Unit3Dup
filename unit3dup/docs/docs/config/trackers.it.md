# Tracker

Sezione `tracker_config` di `Unit3Dbot.json`.

## Le tre chiavi di ogni tracker

Per ogni tracker supportato (`ITT`, `SIS`, `PTT`, `AST`) esistono tre chiavi:

| Chiave | Cos'è | Dove si trova |
|---|---|---|
| `*_URL` | Indirizzo del tracker | Già precompilato nel file di default |
| `*_APIKEY` | La tua API key personale | Sul tracker: profilo utente → impostazioni → API |
| `*_PID` | La tua passkey (PID) | Sul tracker: pagina sicurezza del profilo |

Esempio per ITT:

```json
"ITT_URL": "https://itatorrents.xyz",
"ITT_APIKEY": "la_tua_api_key",
"ITT_PID": "la_tua_passkey",
```

- **`APIKEY`** serve per ogni comunicazione col tracker: upload, ricerche, controllo duplicati
- **`PID`** serve per generare l'announce URL del torrent: è **obbligatoria per ogni tracker presente in `MULTI_TRACKER`** — senza, il bot esce con `-> No PID value`

## MULTI_TRACKER

```json
"MULTI_TRACKER": ["itt", "sis", "ptt", "ast"],
```

La lista dei tracker che il bot conosce e usa:

- Il **primo elemento** è il tracker di **default**: usato quando non passi `-tracker` e per tutti i comandi di [ricerca](../usage/search.md)
- Con `-mt` il bot carica su **tutti** i tracker della lista ([Multi-tracker](../usage/multitracker.md))
- Niente duplicati nella lista, e ogni nome deve essere tra quelli supportati — altrimenti il bot esce con errore

!!! tip "Usi solo ITT?"
    Lascia solo `"MULTI_TRACKER": ["itt"]`: eviti errori di PID mancanti per tracker che non usi.

!!! note "Tracker SIS"
    `SIS_URL` non è precompilato nel file di default: inserisci l'URL del tracker se hai un account.
