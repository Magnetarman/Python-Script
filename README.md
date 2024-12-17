# Python-Script

Script Python Utili. Gli script sono testati personalmente ed utilizzati giornalmente. Se incontrate errori o problemi aprite una issue.

**Attenzione !!!**
Prima di eseguire gli script assicurati di aver installato Python.

[Download Python For Windows](https://www.python.org/downloads/)

# Autore 📈

Creato con ❤️ da [Magnetarman](magnetarman.com), potenziato da ChatGPT e grazie ad [Antonio Porcelli](https://progressify.dev/) per avermi inizializzato allo scrivere e capire Python.

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

### Requisiti 📦

Assicurati di avere installato:

- **Python 3.6+**
- **Pillow**: Per l'elaborazione delle immagini.
- **scikit-learn**: Per il clustering KMeans.
- **Matplotlib**: Per la generazione grafica delle palette.
- **NumPy**: Per la gestione e l'elaborazione delle immagini.

Installa le dipendenze con:

```bash
pip install pillow scikit-learn matplotlib numpy
```

---

### Installazione 🔧

1. Clona questa repository:

```bash
git clone https://github.com/tuo-username/Estrattore-Colori.git
cd Estrattore-Colori
```

2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

---

### Utilizzo 🚀

Esegui lo script dal terminale o da un IDE Python:

```bash
python color_palette.py
```

Segui le istruzioni a schermo per inserire il percorso dell'immagine.

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

### Licenza 📜

Questo progetto è concesso sotto licenza **MIT**. Sentiti libero di utilizzarlo, modificarlo e condividerlo!

---

### Note 📝

- **Formati supportati**: .jpg, .png, .bmp e altri formati compatibili con Pillow.
- **Suggerimento**: Per risultati ottimali, usa immagini con colori chiari e ben definiti.
- Il numero di colori è modificabile cambiando il parametro **num_colors** nello script.

---

## _Trova e Cancella Cartelle Vuote_ - **EFolder.py** 🗂️

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

### Requisiti 📦

Assicurati di avere installato:

- **Python 3.6+**

Lo script utilizza solo moduli della libreria standard di Python, quindi non è necessaria alcuna installazione aggiuntiva.

---

### Installazione 🔧

1. Clona questa repository:

```bash
git clone https://github.com/tuo-username/Trova-Cartelle-Vuote.git
cd Trova-Cartelle-Vuote
```

2. Esegui lo script direttamente:

```bash
python EFolder.py
```

---

### Utilizzo 🚀

Esegui lo script dal terminale o da un IDE Python:

```bash
python EFolder.py
```

Segui le istruzioni per inserire il percorso della cartella da analizzare.

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

### Licenza 📜

Questo progetto è concesso sotto licenza **MIT**. Sentiti libero di utilizzarlo, modificarlo e condividerlo!

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

### Requisiti 📦

Assicurati di avere installato:

- **Python 3.6+**

Lo script utilizza solo moduli della libreria standard di Python, quindi non è necessaria alcuna installazione aggiuntiva.

---

### Installazione 🔧

1. Clona questa repository:

```bash
git clone https://github.com/tuo-username/Elenco-Cartelle-Primo-Livello.git
cd Elenco-Cartelle-Primo-Livello
```

2. Esegui lo script direttamente:

```bash
python elenco_cartelle.py
```

---

### Utilizzo 🚀

Esegui lo script dal terminale o da un IDE Python:

```bash
python elenco_cartelle.py
```

Segui le istruzioni per inserire il percorso della cartella da analizzare.

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

### Licenza 📜

Questo progetto è concesso sotto licenza **MIT**. Sentiti libero di utilizzarlo, modificarlo e condividerlo!

---

### Note 📝

- **Percorsi validi**: Verifica che il percorso inserito esista e sia una directory valida.
- **Output non distruttivo**: Lo script non modifica i contenuti della directory.

---

## _Estensioni dei File in una Cartella_ - **Estensioni.py** 🗂️

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

### Requisiti 📦

Assicurati di avere installato:

- **Python 3.6+**

Lo script utilizza solo moduli della libreria standard di Python, quindi non è necessaria alcuna installazione aggiuntiva.

---

### Installazione 🔧

1. Clona questa repository:

```bash
git clone https://github.com/tuo-username/Estensioni-File.git
cd Estensioni-File
```

2. Esegui lo script direttamente:

```bash
python Estensioni.py
```

---

### Utilizzo 🚀

Esegui lo script dal terminale o da un IDE Python:

```bash
python Estensioni.py
```

Segui le istruzioni per inserire il percorso della cartella da analizzare.

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

### Licenza 📜

Questo progetto è concesso sotto licenza **MIT**. Sentiti libero di utilizzarlo, modificarlo e condividerlo!

---

### Note 📝

- **Percorsi validi**: Verifica che il percorso inserito esista e sia una directory valida.
- **Senza duplicati**: Ogni estensione viene mostrata una sola volta.
- **Ricorsivo**: Esplora anche le sottocartelle.

---

## _Pulizia File Non Musicali_ - **Remove.py** 🗑️

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

### Requisiti 📦

Assicurati di avere installato:

- **Python 3.6+**

Lo script utilizza solo moduli della libreria standard di Python, quindi non è necessaria alcuna installazione aggiuntiva.

---

### Installazione 🔧

1. Clona questa repository:

```bash
git clone https://github.com/tuo-username/Pulizia-File-Musicali.git
cd Pulizia-File-Musicali
```

2. Esegui lo script direttamente:

```bash
python Remove.py
```

---

### Utilizzo 🚀

Esegui lo script dal terminale o da un IDE Python:

```bash
python Remove.py
```

Segui le istruzioni per inserire il percorso della cartella da analizzare.

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

### Licenza 📜

Questo progetto è concesso sotto licenza **MIT**. Sentiti libero di utilizzarlo, modificarlo e condividerlo!

---

### Note 📝

- **Formati supportati**: Lo script conserva solo file con estensioni `.flac`, `.opus`, `.mp3`, `.m4a`, `.aac`.
- **Percorsi validi**: Verifica che il percorso inserito sia corretto e accessibile.
- **Rimozione sicura**: Le cartelle vuote vengono eliminate solo se completamente prive di contenuti.

---
