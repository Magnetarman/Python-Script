# _Convertitore PNG in JPEG_ - **png_converter.py** 🖼️➡️🖼️

Uno script Python che converte automaticamente tutte le immagini `.png` in `.jpg` all'interno di una cartella (e sottocartelle), gestendo correttamente anche le immagini con trasparenza.

---

## Descrizione 📄

Il **Convertitore PNG in JPEG** esplora ricursivamente una cartella e converte ogni immagine `.png` in formato `.jpg`. Le immagini con trasparenza vengono adattate con sfondo bianco per mantenere la compatibilità JPEG.

Utile per:

- **Ottimizzare immagini per il web**.
- **Rimuovere trasparenze** non supportate da JPEG.
- **Convertire rapidamente** grandi quantità di immagini `.png`.

---

## Funzionalità 🌟

- **Conversione ricorsiva**: esplora tutte le sottocartelle.
- **Sfondo bianco automatico**: per PNG con trasparenza.
- **Eliminazione automatica dei PNG**: dopo la conversione, il file originale viene eliminato.
- **Log in tempo reale**: stampa in console i file convertiti e eventuali errori.

---

## Esempio di Utilizzo 🧪

### Avvia lo script:

```bash
python png_to_jpeg.py
```

### Inserisci il percorso della cartella da analizzare quando richiesto:

```plaintext
Inserisci il percorso della cartella da analizzare: /percorso/cartella
```

### Al termine, vedrai un riepilogo dei file convertiti:

```plaintext
[✔] Convertito: /img/foto1.png → /img/foto1.jpg
[✔] Convertito: /img/foto2.png → /img/foto2.jpg
```

---

## Note 📝

- Le immagini `.png` vengono eliminate dopo la conversione.
- Le immagini `.png` con trasparenza avranno sfondo bianco.
- Lo script supporta anche immagini in modalità LA, RGBA, RGB, L.

---
