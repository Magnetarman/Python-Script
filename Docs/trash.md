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
