# Python-Script

Script Python Utili. Gli script sono testati personalmente ed utilizzati giornalmente. Se incontrate errori o problemi aprite una issue.

**Attenzione !!!**
Prima di eseguire gli script assicurati di aver installato Python.

[Download Python For Windows](https://www.python.org/downloads/)

---

## EFolder.py

_Questo script Python permette di trovare e cancellare cartelle vuote all'interno di una directory specificata dall'utente._

### Funzionalità

- Cerca ricorsivamente tutte le cartelle vuote all'interno della directory specificata.
- Stampa l'elenco delle cartelle vuote trovate.
- Chiede all'utente se desidera procedere con la cancellazione delle cartelle vuote trovate.
- Cancella le cartelle vuote se l'utente conferma.

### Utilizzo

- Clona questo repository o scarica lo script find_empty_directories.py.
- Esegui lo script utilizzando Python:

```sh
python Efolder.py
```

### Esempio di Esecuzione

- Inserisci il percorso della cartella che desideri esaminare quando richiesto.
- Lo script mostrerà un elenco delle cartelle vuote trovate e chiederà se desideri cancellarle.

```sh
$ python EFolder.py
Inserisci il percorso della cartella: /path/to/your/folder
Cartelle vuote trovate:
/path/to/your/folder/empty_folder1
/path/to/your/folder/empty_folder2

Numero totale di cartelle vuote trovate: 2
Vuoi procedere con la cancellazione delle cartelle vuote? (y/n): y
Cancellato: /path/to/your/folder/empty_folder1
Cancellato: /path/to/your/folder/empty_folder2
```

### Struttura del Codice

- find_empty_directories(folder_path): Questa funzione cerca tutte le cartelle vuote all'interno della directory specificata.
- print_and_delete_empty_dirs(empty_dirs): Questa funzione stampa le cartelle vuote trovate e, su conferma dell'utente, le cancella.
- main(): La funzione principale che gestisce l'input dell'utente e coordina l'esecuzione delle altre funzioni.

### Note

- **Assicurati di avere i permessi necessari per cancellare le cartelle all'interno della directory specificata.**
- **Usa questo script con cautela per evitare di cancellare cartelle per errore.**

---

## Estensioni.py

_Questo script Python permette di ottenere e stampare tutte le estensioni dei file presenti in una directory specificata dall'utente._

### Funzionalità

- Cerca ricorsivamente tutte le estensioni dei file all'interno della directory specificata.
  Stampa l'elenco delle estensioni trovate, ordinate alfabeticamente.

## Utilizzo

- Clona questo repository o scarica lo script Estensioni.py.
- Esegui lo script utilizzando Python:

```sh
python Estensioni.py
```

- Inserisci il percorso della cartella che desideri esaminare quando richiesto.
- Lo script mostrerà un elenco delle estensioni dei file trovate nella directory specificata.

### Esempio di Esecuzione

```sh
$ python Estensioni.py
Inserisci il percorso della cartella: /path/to/your/folder
Estensioni dei file trovate:
.csv
.jpg
.png
.txt
.zip
```

### Struttura del Codice

- get_file_extensions(folder_path): Questa funzione cerca tutte le estensioni dei file all'interno della directory specificata e le raccoglie in un set per evitare duplicati.
- print_extensions(extensions): Questa funzione stampa l'elenco delle estensioni dei file trovate, ordinate alfabeticamente.
- main(): La funzione principale che gestisce l'input dell'utente e coordina l'esecuzione delle altre funzioni.

---

## Revome.py

_Questo script Python permette di eliminare tutti i file non musicali e le cartelle vuote all'interno di una directory specificata dall'utente. Mantiene solo i file con estensioni musicali specificate (.flac, .opus, .mp3, .m4a, .aac)._

### Funzionalità

- Elimina tutti i file che non hanno un'estensione musicale specificata.
- Elimina tutte le cartelle vuote dopo la rimozione dei file.

### Utilizzo

- Clona questo repository o scarica lo script Remove.py.
- Esegui lo script utilizzando Python:

```sh
python Remove.py
```

- Inserisci il percorso della cartella che desideri pulire quando richiesto.
- Lo script eliminerà tutti i file non musicali e le cartelle vuote all'interno della directory specificata.

### Esempio di Esecuzione

```sh
$ python Remove.py
Inserisci il percorso della cartella: /path/to/your/folder
Deleting file: /path/to/your/folder/document.txt
Deleting file: /path/to/your/folder/image.jpg
Deleting empty directory: /path/to/your/folder/empty_folder
Pulizia completata.
```

### Struttura del Codice

- musical_extensions: Una regex che definisce le estensioni dei file musicali da preservare.
- delete_non_music_files(folder_path): Questa funzione elimina tutti i file non musicali e le cartelle vuote all'interno della directory specificata.
- main(): La funzione principale che gestisce l'input dell'utente e coordina l'esecuzione della funzione di pulizia.

### Note

- **Assicurati di avere i permessi necessari per cancellare le cartelle all'interno della directory specificata.**
- **Usa questo script con cautela per evitare di cancellare cartelle/File per errore.**

---

## Sposta_File.py

_Questo script Python permette di spostare tutti i file presenti nelle sottocartelle di una directory specificata dall'utente alla directory principale stessa. Una volta spostati i file, lo script elimina le sottocartelle vuote._

### Funzionalità

- Sposta tutti i file dalle sottocartelle alla directory principale.
- Elimina le sottocartelle vuote dopo aver spostato i file.
- Ignora i file che già esistono nella directory principale.

### Utilizzo

- Clona questo repository o scarica lo script Sposta_File.py.
- Esegui lo script utilizzando Python:

```sh
python Sposta_File.py
Inserisci il percorso della directory principale che desideri pulire quando richiesto.
```

- Lo script sposterà tutti i file dalle sottocartelle alla directory principale e rimuoverà le sottocartelle vuote.

### Esempio di Esecuzione

```sh
$ python Sposta_File.py
Inserisci il percorso della directory principale: /path/to/your/main_directory
Directory principale: /path/to/your/main_directory
Trovati 10 file da spostare.
Spostando '/path/to/your/main_directory/subfolder1/file1.txt' a '/path/to/your/main_directory/file1.txt'
Spostando '/path/to/your/main_directory/subfolder2/file2.txt' a '/path/to/your/main_directory/file2.txt'
...
10 file sono stati spostati alla directory principale.
Rimuovendo directory vuota '/path/to/your/main_directory/subfolder1'
Rimuovendo directory vuota '/path/to/your/main_directory/subfolder2'
...
5 sottocartelle vuote sono state rimosse.
Operazione completata.
```

### Struttura del Codice

- move_files_to_main_directory(main_directory): Questa funzione sposta tutti i file dalle sottocartelle alla directory principale e rimuove le sottocartelle vuote.
- Il percorso della directory principale viene richiesto all'utente e passato alla funzione move_files_to_main_directory.

### Note

- **Assicurati di avere i permessi necessari per cancellare le cartelle all'interno della directory specificata.**
- **Usa questo script con cautela per evitare di cancellare cartelle/File per errore.**

---

## Transcribe_wav.py

_Questo script Python utilizza il modello Whisper di OpenAI per trascrivere file audio di podcast in testo. I file di trascrizione vengono salvati nella stessa directory dei file audio originali._

### Funzionalità

- Trascrive file audio .wav presenti in una directory specificata.
- Salva le trascrizioni in file di testo con lo stesso nome dei file audio.
- Verifica se una trascrizione esiste già per evitare di ripetere il processo.
- Utilizza il modello Whisper di OpenAI per la trascrizione.

### Utilizzo

- Clona questo repository o scarica lo script Transcribe_wav.py.
- Installiamo e configuriamo FFmpeg:

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

- Assicurati di avere il modello Whisper di OpenAI installato. Puoi installarlo utilizzando:

```sh
pip install openai-whisper pydub
pip --version

# Crea l'ambiente virtuale
python -m venv myenv

# Attiva L'ambiente Virtuale
myenv\Scripts\activate

# Check Attivazione Ambiente Virtuale
pip install openai-whisper pydub

# Verifica l'installazione di FFmpeg
ffmpeg -version
```

- Esegui lo script utilizzando Python:

```sh
python Transcribe_wav.py

Inserisci il percorso della cartella contenente i file audio dei podcast quando richiesto.
```

- Lo script trascriverà i file audio .wav e salverà le trascrizioni nella stessa directory.

### Esempio di Esecuzione

```sh
$ python Transcribe_wav.py
Inserisci il percorso della cartella contenente i podcast: /path/to/your/podcast_directory
Trascrizione in corso per podcast1.wav...
Trascrizione completata per podcast1.wav, salvata in /path/to/your/podcast_directory/podcast1.txt
Trascrizione in corso per podcast2.wav...
Trascrizione completata per podcast2.wav, salvata in /path/to/your/podcast_directory/podcast2.txt
...
Trascrizione completata.
```

### Struttura del Codice

- Transcribe_wav(file_path, model_name='medium', language='it'): Questa funzione carica il modello Whisper e trascrive l'audio del file specificato.
  save_transcription(transcription, output_path): Questa funzione salva la trascrizione in un file di testo.
- main(podcast_dir): La funzione principale che gestisce la scansione della directory dei podcast, la trascrizione dei file audio e il salvataggio delle trascrizioni.

### Note

- Se hai dei comuni file ".mp3" vanno convertiti in wav prima di eseguire lo script [QUI](https://www.mediahuman.com/it/audio-converter/) un software che uso spesso free e di facile utilizzo per la conversione dei file audio
