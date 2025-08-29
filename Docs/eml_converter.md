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
