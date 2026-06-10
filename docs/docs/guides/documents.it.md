# Documenti PDF

Il bot carica anche **documenti PDF** (categoria *edicola*: riviste, fumetti, libri…): estrae la cover dalla prima pagina e la mette nella descrizione del torrent.

## Requisito: Poppler

L'estrazione della cover usa `pdftocairo` (Poppler):

- **Windows**: [installazione Poppler](../install/windows.md#2-poppler-solo-per-i-pdf)
- **Linux**: `sudo apt install poppler-utils`

Verifica:

```bash
pdftocairo -v
```

## Upload

Identico ai video:

```bash
unit3dup -u "/percorso/rivista.pdf"
unit3dup -scan "/percorso/cartella/riviste"
```

Cosa fa il bot:

1. Riconosce il PDF e crea un **oggetto Documenti**
2. Converte la **prima pagina in PNG** con `pdftocairo`
3. Carica la cover sull'[image host](../config/imagehosts.md) e la inserisce nella descrizione
4. Crea il torrent, lo carica, avvia il seeding

Se la categoria non viene riconosciuta dal nome del file, forzala:

```bash
unit3dup -force edicola -u "/percorso/file.pdf"
```

## Le proprietà dell'oggetto Documenti

`name`, `tmdb`, `category_id`, `anonymous`, `description`, `type_id`, `resolution_id`, `personal_release` — come per i [video](../index.md#oggetto-documenti), ma `tmdb` e `resolution_id` sono impostati a valori neutri: il tracker li richiede obbligatori anche quando non hanno senso per un documento.
