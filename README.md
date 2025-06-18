# Python-Script

Script Python Utili. Gli script sono testati personalmente ed utilizzati giornalmente. Se incontrate errori o problemi aprite una issue.

**Versione 3.0** - Nuovo approccio all'esecuzione: non si esegue più uno script isolato, ma tramite un unico punto d’ingresso interattivo.

> [!Note] > Attenzione !!!
> Prima di eseguire gli script assicurati di aver installato Python.

[Download Python For Windows](https://www.python.org/downloads/)

Oppure:

1. Clona questa repository:

```bash
git clone https://github.com/Magnetarman/Python-Script/
```

2. Lancia lo script di installazione:

```powershell
./install.ps1
```

---

## Avvio Wrapper 🔧

**Se hai già python installato e configurato:**

1. Clona questa repository:

```bash
git clone https://github.com/Magnetarman/Python-Script/
```

2. Lancia il Wrapper:

```bash
py main.py
```

3. Segui le istruzioni a schermo per la scelta e l'utilizzo dei vari script

---

## Aggiornamento Automatico _requirements.txt_

![Update requirements.txt](https://github.com/Magnetarman/Python-Script/actions/workflows/update-reqs.yml/badge.svg)

---

## Novità della Versione 3.0

- **Punto unificato:**\
  Introdotto il file `main.py` che gestisce:

  - L'installazione automatica delle dipendenze dal file `requirements.txt`.
  - Un menu interattivo per scegliere quale script eseguire.
  - Organizzazione automatica degli script in ordine alfabetico.
  - Breve descrizione affiancata a ciascuno script.

- **Riorganizzazione della repository:**\
  Migliore gestione e chiarezza degli strumenti disponibili.

---

---

## _Script Disponibili_

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

## _Estrattore di Colori Dominanti_ - **color_palette.py** 🎨

Uno script Python che estrae i **colori dominanti** da un'immagine utilizzando il **clustering KMeans** e li visualizza come una palette. Lo script semplifica immagini complesse nei colori più rappresentativi e salva il risultato come una palette PDF.

---

### Descrizione 📄

L'**Estrattore di Colori Dominanti** analizza un'immagine di input, identifica i colori predominanti utilizzando **KMeans** (machine learning) e genera una **palette visiva chiara** salvata come PDF.

Utile per:

- Designer alla ricerca di ispirazione cromatica.
- Identificare i colori principali in una foto o immagine.
- Generare palette cromatiche per progetti creativi e grafici.

---

### Funzionalità 🌟

- **Estrazione automatica dei colori**: Rileva i primi N colori dominanti (default: 4).
- **Supporto immagini versatile**: Gestisce formati RGB, RGBA e scala di grigi.
- **Visualizzazione intuitiva**: Crea una palette con codici **HEX** chiari e leggibili.
- **Output in PDF**: Salva la palette cromatica come file **color_palette.pdf**.

---

#### Esempio Input

```plaintext
Please enter the path to the image: /percorso/immagine.jpg
```

Lo script elaborerà l'immagine, estrarrà i colori dominanti e salverà la palette cromatica come **color_palette.pdf** nella stessa cartella dell'immagine di input.

---

### Esempio 📊

#### Immagine di Input

Un esempio di immagine (es. tramonto.jpg):  
![Esempio Immagine](https://via.placeholder.com/300x200.png?text=Esempio+Immagine)

#### Palette di Output

La palette generata viene visualizzata con i colori dominanti e i relativi codici **HEX**:

```plaintext
Palette Colori:
------------------------------
Colore 1: #FF5733
Colore 2: #C70039
Colore 3: #900C3F
Colore 4: #581845
```

![Esempio Palette](https://via.placeholder.com/400x100.png?text=Palette+Colori)

---

### Output 💽

La palette cromatica viene salvata come file PDF:

```plaintext
/percorso/immagine/color_palette.pdf
```

Ogni colore è etichettato con il relativo codice **HEX** per una facile consultazione.

---

### Note 📝

- **Formati supportati**: .jpg, .png, .bmp e altri formati compatibili con Pillow.
- **Suggerimento**: Per risultati ottimali, usa immagini con colori chiari e ben definiti.
- Il numero di colori è modificabile cambiando il parametro **num_colors** nello script.

---

## _Trova e Cancella Cartelle Vuote_ - **efolder.py** 🗂️

Uno script Python per individuare e cancellare **cartelle vuote** all'interno di una directory specificata. Lo script esplora ricorsivamente tutte le sottocartelle e fornisce un elenco di quelle vuote, con l'opzione di eliminarle in modo sicuro.

---

### Descrizione 📄

L'**Utility Trova e Cancella Cartelle Vuote** analizza una cartella specificata dall'utente, individua tutte le cartelle vuote e chiede se eliminarle. Questo strumento è utile per:

- **Ottimizzare lo spazio** rimuovendo directory non necessarie.
- **Pulizia automatica** di cartelle generate in fase di sviluppo o backup.
- **Organizzazione** di sistemi di file complessi.

Lo script è interattivo e consente di **confermare l'eliminazione** delle cartelle vuote prima di procedere.

---

### Funzionalità 🌟

- **Scansione ricorsiva**: Esplora tutte le sottocartelle di una directory.
- **Identificazione cartelle vuote**: Elenco chiaro delle directory senza file.
- **Interattivo**: Chiede conferma prima di procedere con la cancellazione.
- **Output dettagliato**: Mostra le cartelle vuote trovate e quelle eliminate.

---

#### Esempio Input

```plaintext
Inserisci il percorso della cartella: /percorso/cartella
```

Lo script analizzerà la cartella e mostrerà tutte le cartelle vuote trovate, chiedendo se procedere con la loro eliminazione.

---

### Output 📊

#### Cartelle Trovate

```plaintext
Cartelle vuote trovate:
/percorso/cartella1
/percorso/subfolder/cartella2

Numero totale di cartelle vuote trovate: 2
```

#### Cancellazione Confermata

Se confermi l'eliminazione:

```plaintext
Cancellato: /percorso/cartella1
Cancellato: /percorso/subfolder/cartella2
```

Se scegli di non procedere:

```plaintext
Operazione annullata.
```

---

### Note 📝

- **Uso responsabile**: Verifica sempre il percorso inserito per evitare eliminazioni involontarie.
- **Sicuro**: Lo script non elimina file, solo cartelle vuote.

---

## _Elenco Cartelle di Primo Livello_ - **elenco_cartelle.py** 🗂️

Uno script Python che elenca tutte le **cartelle di primo livello** in una directory specificata dall'utente e salva i risultati in un file di testo.

---

### Descrizione 📄

L'**Elenco Cartelle di Primo Livello** esplora una directory fornita dall'utente e rileva tutte le cartelle contenute al suo interno (escludendo i file). I risultati vengono salvati automaticamente in un file **cartelle_primo_livello.txt** nella stessa directory analizzata.

Utile per:

- **Organizzare file e cartelle** in sistemi complessi.
- **Raccogliere un elenco delle sottocartelle** per analisi o report.
- **Verificare rapidamente la struttura** di una directory.

---

### Funzionalità 🌟

- **Scansione mirata**: Elenca solo le cartelle di primo livello.
- **Output organizzato**: Salva l'elenco delle cartelle in un file di testo.
- **Semplice e veloce**: Input interattivo con percorsi verificati.
- **Output sicuro**: Non modifica o elimina alcun file o cartella.

---

#### Esempio Input

```plaintext
Inserisci il percorso: /percorso/cartella
```

Lo script analizzerà il percorso inserito e salverà l'elenco delle cartelle di primo livello in un file **cartelle_primo_livello.txt**.

---

### Output 📊

#### Output Terminale

```plaintext
Risultati salvati in: /percorso/cartella/cartelle_primo_livello.txt
```

#### Contenuto del File di Output

```plaintext
Cartelle di primo livello:
/percorso/cartella1
/percorso/cartella2
/percorso/cartella3
```

Il file **cartelle_primo_livello.txt** verrà generato nella stessa cartella specificata come input.

---

### Note 📝

- **Percorsi validi**: Verifica che il percorso inserito esista e sia una directory valida.
- **Output non distruttivo**: Lo script non modifica i contenuti della directory.

---

## _Convertitore di Email in PDF 📧➡️📄_ - **eml_converter.py** 🗂️

Uno script Python per convertire file **.eml** (email salvate) in file **PDF**, mantenendo i dettagli importanti del messaggio come oggetto, mittente, destinatario e contenuto del corpo.

---

## Descrizione 📄

Questo **Convertitore di Email in PDF** esplora una cartella specificata dall'utente, trasforma i file **.eml** in HTML leggibile e poi li converte in file **PDF** salvati in una directory dedicata.

Utile per:

- **Archiviazione email** in un formato facilmente consultabile.
- **Creazione di report** PDF di comunicazioni importanti.
- **Automatizzare** il processo di conversione email in PDF.

---

## Funzionalità 🌟

- **Conversione automatica**: Legge file **.eml**, genera un HTML e lo salva come PDF.
- **Output organizzato**: Salva tutti i PDF in una cartella dedicata chiamata **converted_pdfs**.
- **Dettagli inclusi**: Oggetto, mittente, destinatario e corpo del messaggio preservati nel PDF.

---

## Requisiti 📦

- **wkhtmltopdf**: Strumento esterno necessario per generare PDF. Scaricalo e installalo dal sito ufficiale: [wkhtmltopdf.org](https://wkhtmltopdf.org/).

---

### Esempio Output

```plaintext
Inserisci il percorso della cartella contenente i file .eml: /percorso/della/cartella
Converted: email1.eml -> /percorso/della/cartella/converted_pdfs/email1.pdf
Converted: email2.eml -> /percorso/della/cartella/converted_pdfs/email2.pdf
Tutti i file .eml sono stati convertiti in PDF nella cartella 'converted_pdfs'.
```

---

## Note 📝

- **Formati supportati**: Lo script funziona con file **.eml** standard.
- **Percorsi validi**: Assicurati di fornire un percorso esistente e accessibile.
- **Output pulito**: Ogni PDF include i dettagli dell'email in un formato leggibile.

---

## _Estensioni dei File in una Cartella_ - **estensioni.py** 🗂️

Uno script Python che analizza una directory specificata dall'utente ed elenca tutte le **estensioni dei file** presenti, escludendo duplicati e organizzandole in ordine alfabetico.

---

### Descrizione 📄

L'**Estensione dei File in una Cartella** esplora una directory fornita dall'utente e rileva tutte le estensioni dei file (es. `.txt`, `.jpg`, `.pdf`). Questo strumento è utile per:

- **Organizzare** e analizzare rapidamente i tipi di file in una cartella.
- **Identificare formati presenti** per pulizie o analisi dei dati.
- **Controllare tipi di file** in sistemi di archiviazione complessi.

Lo script stampa le estensioni trovate direttamente nel terminale.

---

### Funzionalità 🌟

- **Scansione ricorsiva**: Esplora tutti i file nella cartella e sottocartelle.
- **Filtraggio intelligente**: Elimina duplicati e considera solo estensioni valide.
- **Ordinamento alfabetico**: Organizza le estensioni per una lettura chiara.
- **Semplicità d'uso**: Input interattivo e output pulito.

---

#### Esempio Input

```plaintext
Inserisci il percorso della cartella: /percorso/cartella
```

Lo script analizzerà la cartella e stamperà le estensioni dei file trovate.

---

### Output 📊

#### Output Terminale

```plaintext
Estensioni dei file trovate:
.csv
.jpg
.pdf
.png
.txt
```

Le estensioni vengono visualizzate in ordine alfabetico per una lettura chiara e organizzata.

---

### Note 📝

- **Percorsi validi**: Verifica che il percorso inserito esista e sia una directory valida.
- **Senza duplicati**: Ogni estensione viene mostrata una sola volta.
- **Ricorsivo**: Esplora anche le sottocartelle.

---

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

# _Convertitore PNG in JPEG_ - **png_to_jpeg.py** 🖼️➡️🖼️

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

## _Pulizia File Non Musicali_ - **remove.py** 🗑️

Uno script Python che elimina tutti i file non musicali in una directory specificata dall'utente e rimuove eventuali cartelle vuote.

---

### Descrizione 📄

L'**Utility di Pulizia File Non Musicali** esplora una cartella e le sue sottocartelle, identificando e **rimuovendo i file non musicali** (basandosi sulle estensioni dei file). Inoltre, lo script elimina automaticamente le cartelle vuote trovate durante la scansione.

Utile per:

- **Organizzare librerie musicali** rimuovendo file indesiderati.
- **Pulire sistemi di archiviazione** mantenendo solo i file musicali.
- **Risparmiare spazio** eliminando file non necessari.

---

### Funzionalità 🌟

- **Scansione ricorsiva**: Analizza tutte le cartelle e sottocartelle.
- **Criterio intelligente**: Mantiene solo file con estensioni musicali (flac, opus, mp3, m4a, aac).
- **Rimozione sicura**: Elimina solo file non conformi e cartelle vuote.
- **Output dettagliato**: Mostra i file e le cartelle eliminate.

---

#### Esempio Input

```plaintext
Inserisci il percorso della cartella: /percorso/cartella
```

Lo script analizzerà la cartella e rimuoverà tutti i file non musicali e le cartelle vuote.

---

### Output 📊

#### Output Terminale

```plaintext
Deleting file: /percorso/cartella/file1.txt
Deleting file: /percorso/cartella/subfolder/file2.docx
Deleting empty directory: /percorso/cartella/subfolder
Pulizia completata.
```

Tutti i file non conformi vengono eliminati e il percorso è mostrato chiaramente nel terminale.

---

### Note 📝

- **Formati supportati**: Lo script conserva solo file con estensioni `.flac`, `.opus`, `.mp3`, `.m4a`, `.aac`.
- **Percorsi validi**: Verifica che il percorso inserito sia corretto e accessibile.
- **Rimozione sicura**: Le cartelle vuote vengono eliminate solo se completamente prive di contenuti.

---

## _Spostamento File nelle Directory Principali_ - **sposta_file.py** 🚚

Uno script Python che sposta tutti i file dalle sottocartelle alla **directory principale** specificata, eliminando le cartelle vuote una volta completata l'operazione.

---

### Descrizione 📄

L'**Utility di Spostamento File** esplora una directory e le sue sottocartelle, spostando **tutti i file** trovati direttamente nella cartella principale. Dopo aver spostato i file, lo script elimina automaticamente le cartelle vuote.

Utile per:

- **Organizzare** i file sparsi in sottocartelle.
- **Centralizzare i contenuti** in una cartella principale.
- **Pulire cartelle vuote** per ottimizzare la struttura dei file.

---

### Funzionalità 🌟

- **Spostamento ricorsivo**: Trova e sposta i file da tutte le sottocartelle.
- **Gestione conflitti**: Evita sovrascritture saltando i file con lo stesso nome.
- **Rimozione automatica**: Elimina le sottocartelle vuote dopo lo spostamento.
- **Output dettagliato**: Mostra i file spostati e le cartelle eliminate.

---

#### Esempio Input

```plaintext
Inserisci il percorso della directory principale: /percorso/cartella
```

Lo script analizzerà la cartella e sposterà tutti i file dalle sottocartelle alla directory principale.

---

### Output 📊

#### Output Terminale

```plaintext
Trovati 5 file da spostare.
Spostando '/percorso/cartella/subfolder/file1.txt' a '/percorso/cartella/file1.txt'
Spostando '/percorso/cartella/subfolder/file2.docx' a '/percorso/cartella/file2.docx'
Rimuovendo directory vuota '/percorso/cartella/subfolder'
3 file sono stati spostati alla directory principale.
1 sottocartelle vuote sono state rimosse.
Operazione completata.
```

---

### Note 📝

- **Conflitti di nomi**: Se un file con lo stesso nome esiste già nella directory principale, lo script salta quel file.
- **Percorsi validi**: Assicurati che il percorso inserito esista e sia accessibile.
- **Rimozione sicura**: Le cartelle vuote vengono eliminate solo se completamente prive di contenuti.

---

## _Trascrizione Automatica di Podcast_ - **transcribe_wav.py** 🎙️

Uno script Python che converte file audio in formato `.wav`, li trascrive utilizzando **Whisper** di OpenAI e salva il testo risultante in un file `.txt`.

---

### Descrizione 📄

L'**Utility di Trascrizione Podcast** esplora una cartella contenente file audio in vari formati supportati (come `.mp3`, `.flac`, `.ogg`) e:

1. **Converte i file audio** in formato `.wav` (se necessario).
2. **Trascrive il contenuto audio** utilizzando il modello di machine learning Whisper.
3. **Salva la trascrizione** in un file di testo `.txt` nella stessa cartella.

Utile per:

- **Podcaster** che vogliono generare trascrizioni automatiche dei loro contenuti.
- **Trascrizione rapida** di interviste o registrazioni audio.
- **Accessibilità** e archiviazione del contenuto audio in formato testuale.

---

### Funzionalità 🌟

- **Conversione formato**: Supporta `.mp3`, `.flac`, `.ogg` e li converte automaticamente in `.wav`.
- **Trascrizione automatica**: Utilizza il modello Whisper per trascrivere l'audio.
- **Output organizzato**: Salva le trascrizioni come file `.txt` nella stessa directory.
- **Evitare duplicati**: Salta i file già trascritti.

---

Assicurati di avere **FFmpeg** installato sul tuo sistema, necessario per pydub:

- **Windows**: Scarica FFmpeg da [ffmpeg.org](https://ffmpeg.org/)
- **Linux/Mac**: Installa con il package manager appropriato:

```bash
sudo apt install ffmpeg    # Linux
brew install ffmpeg        # MacOS
```

#### Installazione e Configurazione di FFmpeg su Windows

- **Scarica FFmpeg**:
  - Vai su [ffmpeg.org](https://ffmpeg.org/download.html).
  - Clicca su "Download" sotto "More downloading options".
  - Seleziona il link "Windows builds from gyan.dev".
  - Scarica la versione statica (ad esempio, "ffmpeg-release-essentials.zip").
- - **Estrai FFmpeg**:

    - Estrarre il file `ffmpeg-release-essentials.zip` in una directory come `C:\ffmpeg`.

- **Aggiungi FFmpeg al PATH**:
  - Apri "Impostazioni" dal menu Start.
  - Cerca "Environment Variables" e seleziona "Modifica le variabili d'ambiente di sistema".
  - Clicca su "Variabili d'ambiente" nella finestra "Proprietà del sistema".
  - Seleziona `Path` sotto "Variabili di sistema" e clicca su "Modifica...".
  - Clicca su "Nuovo" e inserisci `C:\ffmpeg\bin`.
- **Verifica l'installazione di FFmpeg**:

  - Apri il Prompt dei comandi.
  - Esegui `ffmpeg -version`.

```sh
# Crea l'ambiente virtuale
python -m venv myenv

# Attiva L'ambiente Virtuale
myenv\Scripts\activate

# Check Attivazione Ambiente Virtuale
pip install openai-whisper pydub

# Verifica l'installazione di FFmpeg
ffmpeg -version
```

---

### Esempio Input

```plaintext
Inserisci il percorso della cartella contenente i podcast: /percorso/podcast
```

Lo script analizzerà la cartella, convertirà i file non `.wav` e trascriverà il contenuto audio.

---

## Output 📊

### Output Terminale

```plaintext
Conversione di /percorso/podcast/episodio1.mp3 in formato .wav...
File convertito: /percorso/podcast/episodio1.wav
Trascrizione in corso per episodio1.wav...
Trascrizione completata per episodio1.wav, salvata in /percorso/podcast/episodio1.txt
Saltato episodio2.wav, il file di trascrizione esiste già.
```

### File di Output

Per ogni file audio, viene generato un file `.txt` con la trascrizione:

```plaintext
/percorso/podcast/episodio1.txt
/percorso/podcast/episodio2.txt
```

---

## Note 📝

- **Formati supportati**: `.mp3`, `.flac`, `.ogg`, `.wav`
- **Requisiti hardware**: La trascrizione Whisper potrebbe richiedere una GPU per performance ottimali.
- **Prevenzione duplicati**: Se un file `.txt` esiste già, lo script lo salta.

---

## _Spostamento File con Criteri di Ricerca_ - **trash.py** 🔍

Uno script Python che sposta file con nomi che terminano con uno specifico set di caratteri in una cartella dedicata chiamata **duplicati**, all'interno della stessa directory principale.

---

## Descrizione 📄

L'**Utility di Spostamento File con Criteri** esplora una cartella specificata dall'utente, cerca file i cui nomi terminano con un set di caratteri scelto dall'utente, e li sposta in una cartella **duplicati**.

Utile per:

- **Organizzare** file duplicati o con nomi specifici.
- **Raggruppare contenuti simili** in una cartella dedicata.
- **Pulizia rapida** e archiviazione automatica dei file.

---

## Funzionalità 🌟

- **Selezione dinamica**: Permette di scegliere il set di caratteri da cercare nei nomi dei file.
- **Spostamento automatico**: I file vengono spostati nella cartella **duplicati**.
- **Interfaccia interattiva**: Permette di selezionare la cartella con una finestra di dialogo.
- **Sicuro e organizzato**: Non sovrascrive i file, mantenendo un output ordinato.

---

### Esempio Input

```plaintext
Inserisci il set di caratteri che vuoi cercare alla fine dei nomi dei file: copia
```

Una volta selezionata la cartella principale, lo script analizzerà i file e sposterà quelli con nomi terminanti in "copia" nella cartella **duplicati**.

---

## Output 📊

### Output Terminale

```plaintext
File spostato in 'duplicati': /percorso/cartella/file_copia.txt
File spostato in 'duplicati': /percorso/cartella/subfolder/documento_copia.pdf
Operazione completata!
```

### Cartella di Output

I file spostati saranno salvati nella cartella:

```plaintext
/percorso/cartella/duplicati/
```

---

## Note 📝

- **Criterio di ricerca**: Cerca solo file i cui nomi terminano con il set di caratteri specificato.
- **Percorsi validi**: Assicurati di selezionare una cartella esistente.
- **Output pulito**: I file vengono spostati senza duplicare o sovrascrivere altri contenuti.

---
