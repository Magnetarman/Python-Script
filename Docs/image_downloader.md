## _Scaricatore di Immagini da Pagina Web 🌐🖼️_ - **image_downloader.py** 🗂️

Uno script Python per **scaricare tutte le immagini** presenti in una pagina web, inclusi i contenuti **Base64** convertiti in PNG o nel loro formato originale.

---

## Descrizione 📄

Questo **Image Downloader** analizza il contenuto HTML di una pagina web, individua tutti i tag `<img>` e scarica le immagini collegate nel formato originale. Gestisce sia immagini con URL assoluti e relativi, sia immagini codificate in Base64.

Utile per:

- **Salvare tutte le immagini** da una pagina web con un click.
- **Effettuare scraping visivo** per archiviazione o analisi.
- **Convertire immagini Base64** in file immagine leggibili.

---

## Funzionalità 🌟

- ✅ Rileva immagini standard e in lazy loading (`src`, `data-src`).
- 🧠 Converte immagini Base64 in file reali, inclusi `.png`.
- 📁 Crea automaticamente una cartella `export` per l’output.
- 🔁 Gestisce URL relativi grazie a `urljoin`.
- 🧽 Pulisce gli URL rimuovendo parametri inutili (`?`).

---

### Esempio Output

```plaintext
Inserisci l'URL della pagina web: https://esempio.it
Scaricata: export/logo.png
Scaricata immagine Base64: export/base64_image_1.png
```

---

## Note 📝

- Le immagini SVG in Base64 vengono convertite in `.png`.
- Lo script non scarica risorse dinamiche caricate da JavaScript.
- Funziona solo con pagine accessibili pubblicamente.

---
