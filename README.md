# Python-Script

Script Python Utili.

**Attenzione !!!**
Prima di eseguire gli script assicurati di aver installato Python.

[Windows](https://www.python.org/downloads/)

---

## EFolder.py

_Questo script Python permette di trovare e cancellare cartelle vuote all'interno di una directory specificata dall'utente._

### Funzionalità

- Cerca ricorsivamente tutte le cartelle vuote all'interno della directory specificata.
- Stampa l'elenco delle cartelle vuote trovate.
- Chiede all'utente se desidera procedere con la cancellazione delle cartelle vuote trovate.
  Cancella le cartelle vuote se l'utente conferma.

### Utilizzo

- Clona questo repository o scarica lo script find_empty_directories.py.
- Esegui lo script utilizzando Python:

```sh
python Efolder.py
```

### Esempio di Esecuzione

- Inserisci il percorso della cartella che desideri esaminare quando richiesto.
- Lo script mostrerà un elenco delle cartelle vuote trovate e chiederà se desideri cancellarle.

```
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

Assicurati di avere i permessi necessari per cancellare le cartelle all'interno della directory specificata.
Usa questo script con cautela per evitare di cancellare cartelle per errore.

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
