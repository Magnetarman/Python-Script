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
