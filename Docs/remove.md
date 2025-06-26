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
