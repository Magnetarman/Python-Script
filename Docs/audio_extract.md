## _Estrattore Tracce Audio da MKV 🎥🎵_ - **audio_extract.py** 🗂️

Uno script Python per **identificare** e **estrarre tracce audio** da file `.mkv`, singolarmente o in modo ricorsivo da una cartella. Utilizza `ffprobe` per analizzare le tracce e `ffmpeg` per estrarle nel formato `.flac`.

---

## Descrizione 📄

Questo **Estrattore Audio da MKV** consente di selezionare e salvare una traccia audio specifica da un file `.mkv`, mantenendo la qualità del flusso originale grazie alla conversione in `.flac`.

Utile per:

- **Recuperare tracce audio multilingua** da film e serie.
- **Creare archivi audio** da video in alta qualità.
- **Automatizzare l'estrazione** da intere directory video.

---

## Funzionalità 🌟

- **Analisi automatica**: mostra tutte le tracce audio disponibili con la lingua (se presente).
- **Conversione diretta**: estrae la traccia scelta e la salva come file `.flac`.
- **Supporto directory**: può elaborare cartelle con più file `.mkv`, anche in modo ricorsivo.
- **Interfaccia interattiva**: guida passo dopo passo tramite input da terminale.

---

## Requisiti 📦

- **ffmpeg** (incluso anche `ffprobe`)

> Assicurati che `ffmpeg` e `ffprobe` siano installati e accessibili tramite il terminale (PATH di sistema).

---

## Utilizzo 🚀

### ▶️ Modalità Singolo File

1. Inserisci il percorso di un file `.mkv` quando richiesto.
2. Visualizza le tracce disponibili.
3. Seleziona quella da esportare.

### 📁 Modalità Directory

1. Inserisci il percorso di una cartella.
2. Indica il numero della traccia da estrarre.
3. Scegli se elaborare ricorsivamente le sottocartelle.

### Esempio Output

file audio verranno salvati con il seguente formato:

```
nomefile_trackX.flac
```

Nello **stesso percorso** del video originale, dove `X` è il numero della traccia selezionata.

---

## Esempio di Utilizzo 🧪

### Singolo File:

```plaintext
Inserisci il percorso del file MKV o della directory: /video/film.mkv

Tracce audio trovate:
0: Traccia 0 (ita)
1: Traccia 1 (eng)

Inserisci il numero della traccia da esportare: 1
Audio estratto: /video/film_track1.flac
```

### Cartella:

```plaintext
Inserisci il percorso del file MKV o della directory: /media/serie_tv
Inserisci il numero della traccia da esportare: 0
Vuoi elaborare tutti i file MKV nella directory in modo ricorsivo? (s/n): s
```

---

## Note 📝

- Funziona solo con file `.mkv`.
- L'output è sempre in formato `.flac`, ma lo script può essere adattato ad altri formati (`.mp3`, `.wav`, ecc).
- Le lingue vengono mostrate se disponibili nei metadati.

---
