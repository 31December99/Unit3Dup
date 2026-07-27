# Installazione su Windows

## Requisiti

- **Python 3.10 o superiore** (consigliato: dalla 3.10 alla 3.12 — le versioni più recenti possono dare problemi con alcune librerie)
- **FFmpeg** — usato per estrarre gli screenshot dai video
- **Poppler** — solo se vuoi creare torrent di documenti PDF

## 1. Installa FFmpeg

1. Scarica FFmpeg da [ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)
2. Decomprimi l'archivio in una cartella a piacere (es. `C:\ffmpeg`)
3. Aggiungi la cartella `bin` di FFmpeg alla variabile d'ambiente **PATH** (utente)
4. Chiudi e riapri il terminale, poi verifica:

```bash
ffmpeg -version
```

## 2. Poppler (solo per i PDF)

Serve soltanto se caricherai documenti PDF — il bot lo usa per estrarre la cover dalla prima pagina.

1. Scarica Poppler per Windows da [github.com/oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Decomprimi e aggiungi la cartella `bin` al PATH di sistema (esempio: `C:\poppler-24.08.0\Library\bin`)
3. **Chiudi e riapri il terminale**
4. Verifica l'installazione:

```bash
pdftocairo -v
```

## 3. Installa Unit3Dup

```bash
pip install unit3dup
```

## 4. Primo avvio

```bash
unit3dup
```

!!! note "Messaggi rossi al primo avvio?"
    È normale: il bot ti sta avvisando che non è ancora configurato. Al primo avvio crea la cartella di configurazione e il file `Unit3Dbot.json`. Prosegui con la [Configurazione](../config/intro.md).
