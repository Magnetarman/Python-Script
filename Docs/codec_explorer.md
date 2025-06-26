## _Analizzatore Codec Video_ - **codec_explorer.py** 🎥📊

Uno strumento grafico interattivo Python che esamina ricorsivamente tutti i video in una directory specificata. Per ogni file video con codec H264 o H265, visualizza:

- Nome file
- Codec video
- Risoluzione
- Bitrate stimato (kbps)
- Dimensione del file in GB

---

### Descrizione 📄

L'**Analizzatore Codec Video** è una utility intuitiva che analizza i file multimediali, identificando i codec H264 e H265 (HEVC) e fornendo statistiche tecniche dettagliate.

Utile per:

- Classificare e organizzare collezioni video in base al codec.
- Ottenere rapidamente informazioni tecniche sui propri file multimediali.
- Esportare i dati raccolti per analisi approfondite (Excel/CSV).

---

### Funzionalità 🌟

- **Riconoscimento automatico dei codec**: Identifica e separa i file in base al codec video (H264 o H265/HEVC).
- **Analisi tecnica completa**: Utilizza `ffprobe` per recuperare risoluzione, durata e calcolare il bitrate medio.
- **Interfaccia grafica intuitiva (Tkinter)**: Permette l'esplorazione e la visualizzazione organizzata dei dati.
- **Esportazione semplice**: Salva i risultati in formato `.xlsx` (Excel) o `.csv`.

---

#### Esempio di Utilizzo 🧪

Passaggi:

1.  Clicca su "Seleziona cartella e analizza".
2.  Attendi l'analisi dei file video.
3.  I risultati saranno mostrati in due schede: **Video H264** e **Video H265**.
4.  Per salvare i dati, clicca su "Esporta in Excel o CSV".

---

### Output 📊

I risultati sono organizzati in due tabelle distinte all'interno dell'interfaccia grafica:

#### Video H264

#### Video H265

Ogni riga contiene le seguenti informazioni:

`Nome File` | `Codec` | `Risoluzione` | `Bitrate (kbps)` | `Dimensione (GB)`

---

### Note 📝

- **File supportati**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv` e altri formati compatibili con `ffprobe`.
- Lo script ignora automaticamente i file con codec diversi da H264 o H265.
- Per un funzionamento corretto, `ffprobe` deve essere installato nel sistema.
- ⚠️ **Dipendenza**: Se `ffprobe` non è disponibile, l'analisi dei file fallirà. Si raccomanda di installare `ffmpeg` (che include `ffprobe`) da [ffmpeg.org](https://ffmpeg.org/) o tramite il tuo gestore di pacchetti.

---
