# PDF documents

The bot also uploads **PDF documents** (the *edicola* category: magazines, comics, books…): it extracts the cover from the first page and puts it in the torrent description.

## Requirement: Poppler

Cover extraction uses `pdftocairo` (Poppler):

- **Windows**: [Poppler installation](../install/windows.md#2-poppler-pdf-only)
- **Linux**: `sudo apt install poppler-utils`

Verify:

```bash
pdftocairo -v
```

## Upload

Same as for videos:

```bash
unit3dup -u "/path/magazine.pdf"
unit3dup -scan "/path/magazines/folder"
```

What the bot does:

1. Recognizes the PDF and creates a **Document object**
2. Converts the **first page to PNG** with `pdftocairo`
3. Uploads the cover to the [image host](../config/imagehosts.md) and adds it to the description
4. Creates the torrent, uploads it, starts seeding

If the category isn't recognized from the file name, force it:

```bash
unit3dup -force edicola -u "/path/file.pdf"
```

## Document object properties

`name`, `tmdb`, `category_id`, `anonymous`, `description`, `type_id`, `resolution_id`, `personal_release` — same as [videos](../index.md#document-object), but `tmdb` and `resolution_id` are set to neutral values: the tracker requires them even when they make no sense for a document.
