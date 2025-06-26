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
