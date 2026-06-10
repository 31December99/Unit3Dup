# Reseed

`-reseed` serve a **rimettere in seeding contenuti che hai già sul disco**, partendo da torrent già esistenti sul tracker — senza creare niente di nuovo.

## Come funziona

```bash
unit3dup -reseed -f "/percorso/cartella"
unit3dup -reseed -scan "/percorso/libreria"
```

Per ogni contenuto video trovato nel percorso:

1. Il bot identifica il titolo (ricerca TMDB, come per un upload)
2. Cerca sul tracker un torrent **corrispondente** al tuo file
3. Se lo trova, **scarica il `.torrent` dal tracker** nell'[archivio](../config/options.md#percorsi) (`<archivio>/<TRACKER>/`)
4. Lo consegna al client torrent, che riprende il seeding usando i tuoi file locali

Con più tracker (lista `MULTI_TRACKER` o `-mt`) il giro viene ripetuto per ognuno.

## A cosa serve

- **Riprendere il seeding** di release che avevi già caricato, dopo un cambio di client o di macchina
- **Seedare release esistenti** di cui possiedi già i file identici
- **Migrare tra OS diversi**: i torrent creati su Linux si riseedano su Windows e viceversa

!!! note "Solo contenuti video"
    Il reseed lavora su film e serie; documenti e giochi non sono coinvolti.

!!! tip "Titoli sporchi"
    Se il nome della cartella non basta a identificare il titolo, aggiungi `-notitle "Titolo Vero"`.
