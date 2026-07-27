# Giochi

Per i giochi il bot interroga **IGDB** (Internet Game Database) e trasmette al tracker l'ID del titolo, come fa con TMDB per i film.

## 1. Crea le credenziali IGDB

IGDB appartiene a Twitch: le API si attivano dalla console sviluppatori Twitch.

1. Account su [twitch.tv](https://www.twitch.tv) (con 2FA attiva)
2. Vai su [dev.twitch.tv/console](https://dev.twitch.tv/console) → *Applications* → *Register Your Application*
3. Nome a piacere, OAuth Redirect URL `http://localhost`, categoria *Application Integration*
4. Ottieni **Client ID** e genera il **Client Secret**

## 2. Configura il bot

In `tracker_config` di `Unit3Dbot.json`:

```json
"IGDB_CLIENT_ID": "il_tuo_client_id",
"IGDB_ID_SECRET": "il_tuo_client_secret",
```

!!! warning "Senza credenziali i giochi vengono saltati"
    Con `IGDB_CLIENT_ID` a `no_key` il bot mostra `Skipping game upload, no IGDB credentials provided` e prosegue solo con gli altri contenuti.

## 3. Upload

```bash
unit3dup -f "/percorso/Nome.Gioco.v1.0.REPACK"
unit3dup -force game -f "/percorso/cartella_gioco"
```

Il bot crea un **oggetto Game**: cerca il titolo su IGDB, ricava l'ID (`igdb`) e riconosce la **piattaforma** (PC, console…) per il tag corrispondente. Le altre proprietà (`name`, `category_id`, `description`…) funzionano [come per i video](../index.md#oggetto-game), con `tmdb` a valore neutro.

!!! tip "Categoria non riconosciuta?"
    Se il bot scambia il gioco per un film, forza la categoria con `-force game`.
