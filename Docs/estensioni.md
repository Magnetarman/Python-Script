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
