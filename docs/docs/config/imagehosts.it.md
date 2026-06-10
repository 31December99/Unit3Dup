# Image host

Il bot estrae gli screenshot dal video e li carica su un servizio di hosting immagini; gli URL finiscono nella descrizione del torrent. Le chiavi stanno in `tracker_config`, le priorità in `user_preferences`.

## Host supportati

| Host | Sito | Chiave |
|---|---|---|
| PtScreens | [ptscreens.com](https://ptscreens.com) | `PTSCREENS_KEY` |
| LensDump | [lensdump.com](https://lensdump.com) | `LENSDUMP_KEY` |
| FreeImage | [freeimage.host](https://freeimage.host) | `FREE_IMAGE_KEY` |
| ImgBB | [imgbb.com](https://imgbb.com) | `IMGBB_KEY` |
| ImgFI | [imgfi.com](https://imgfi.com) | `IMGFI_KEY` |
| PassIMA | [passtheima.ge](https://passtheima.ge) | `PASSIMA_KEY` |
| ImaRide | [imageride.net](https://www.imageride.net) | `IMARIDE_KEY` |

Per ogni host: registrati sul sito, genera la API key, incollala in `Unit3Dbot.json`:

```json
"IMGBB_KEY": "la_tua_chiave",
"FREE_IMAGE_KEY": "la_tua_chiave",
```

!!! tip "Quanti host configurare?"
    Non è obbligatorio usarli tutti, ma **configurane almeno due**: se l'upload su un host fallisce, il bot passa automaticamente al successivo.

## Priorità e fallback

In `user_preferences` ogni host ha una priorità — **0 = primo tentativo**:

```json
"PTSCREENS_PRIORITY": 0,
"LENSDUMP_PRIORITY": 1,
"FREE_IMAGE_PRIORITY": 2,
"IMGBB_PRIORITY": 3,
"IMGFI_PRIORITY": 4,
"PASSIMA_PRIORITY": 5,
"IMARIDE_PRIORITY": 6,
```

Il bot tenta gli host in ordine di priorità crescente; al primo errore (chiave non valida, servizio giù, limite raggiunto) passa al successivo.

Le opzioni sugli screenshot (`NUMBER_OF_SCREENSHOTS`, compressione, resize, webp) sono nelle [Opzioni avanzate](options.md).
