## 🖼️ _Generazione PDF da Immagini JPEG_ - **pdf_combiner.py**

Uno script Python con interfaccia grafica che consente di selezionare immagini JPEG e convertirle in un **PDF ottimizzato**, pronto per l’archiviazione o la stampa.

---

## Descrizione 📄

L'**Elaboratore di Documenti Scansionati** permette di importare una o più immagini, migliorarne automaticamente la leggibilità e generare un PDF ordinato e pulito.

Ideale per:

- **Digitalizzare documenti cartacei** in modo rapido.
- **Migliorare la leggibilità** di scansioni non perfette.
- **Creare archivi PDF** partendo da immagini di bassa qualità.

---

## Funzionalità 🌟

- **Correzione orientamento**: Rileva automaticamente la rotazione delle pagine.
- **Pulizia avanzata**: Rimuove bordi, rumore e migliora la leggibilità del testo.
- **Conversione bianco/nero**: Per un output chiaro, leggibile e leggero.
- **Interfaccia intuitiva**: Selezione immagini con un semplice click.
- **Output ordinato**: Salva un PDF nella cartella delle immagini, con nome e data.

---

### Esempio di utilizzo 🧪

1. Avvia lo script.
2. Seleziona una o più immagini `.jpeg` o `.jpg`.
3. Clicca su **"Elabora Documenti"**.
4. Attendi la fine del processo: il PDF sarà generato automaticamente.

---

## Output 📊

### Output PDF

- Nome file: `Documenti_Scansionati_YYYYMMDD_HHMMSS.pdf`
- Posizione: stessa cartella delle immagini originali.

### Output Terminale / Log

```plaintext
Immagine 1/3: Analisi immagine...
Immagine 1/3: Correzione orientamento...
Immagine 1/3: Conversione in bianco e nero...
...
Creazione PDF...
Elaborazione completata!
```

## Note 📝

- Compatibilità: Supporta immagini .jpeg, .jpg e .png.
- Performance: Il processo potrebbe richiedere alcuni secondi per immagine.
- Nitidezza & Contrasto: Le funzioni di aumento sono disabilitate per migliorare la leggibilità del testo.
