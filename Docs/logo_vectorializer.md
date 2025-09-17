## _Vettorializzatore di Loghi con AI 🎨✨_ - **logo_vectorializer.py** 🤖

Uno script Python per **analizzare** e **vettorializzare loghi** da file immagine (`.png`, `.jpeg`, `.svg`). Utilizza l'intelligenza artificiale di **Google Gemini** per ricreare una versione vettoriale `.svg` di alta qualità.

---

## Descrizione 📄

Questo **Vettorializzatore di Loghi** invia un'immagine a Google Gemini e ne richiede una ricostruzione vettoriale _pixel-perfect_, salvandola in formato `.svg` senza sfondo.

Utile per:

- **Modernizzare loghi datati** o disponibili solo in bassa risoluzione.
- **Ottenere una versione scalabile** per stampa, web e design grafico.
- **Automatizzare un processo di conversione** che altrimenti richiederebbe software e competenze specifiche.

---

## Funzionalità 🌟

- **Vettorializzazione AI**: sfrutta la potenza di Google Gemini per un'analisi e una ricostruzione precisa.
- **Supporto multiformato**: accetta in input i formati più comuni (`.png`, `.jpeg`, `.svg`).
- **Output professionale**: genera un file `.svg` pulito, senza sfondo e pronto all'uso.
- **Interfaccia interattiva**: guida l'utente passo dopo passo per inserire il file e la chiave API.
- **Gestione automatica**: nomina e salva il file di output in modo prevedibile.

---

## Requisiti 📦

- **Python 3.x**
- **Libreria `google-generativeai`**
- **Una chiave API di Google Gemini**

> Puoi installare la libreria richiesta con il comando: `pip install google-generativeai`

---

## Utilizzo 🚀

### ▶️ Esecuzione Standard

1.  Avvia lo script dal tuo terminale: `python logo_vectorializer.py`.
2.  Inserisci il **percorso completo** del file del logo quando richiesto.
3.  Incolla la tua **chiave API di Google Gemini**.
4.  Attendi che l'API elabori l'immagine e generi il file.

### Esempio Output

Il file vettoriale verrà salvato nella **stessa cartella in cui si trova lo script** con il seguente formato:

```
nomefileoriginale-Vector.svg
```

Ad esempio, `logo.png` diventerà `logo-Vector.svg`.

---

## Esempio di Utilizzo 🧪

```plaintext
--- Logo Vectorializer con Google Gemini ---
Inserisci il percorso del file immagine (png, jpeg, svg): /Users/mario/Desktop/logo_azienda.png
Inserisci il tuo Google Gemini API token key: AIzaSy*******************

Caricamento dell'immagine...
Invio dell’immagine a Google Gemini in corso...
Attesa della risposta (l'operazione potrebbe richiedere alcuni istanti)...
Salvataggio del file in corso: /Users/mario/scripts/logo_azienda-Vector.svg
------------------------------
✅ Esito finale: SUCCESSO
Logo vettoriale generato con successo: /Users/mario/scripts/logo_azienda-Vector.svg
------------------------------
```

---

## Note 📝

- La qualità del risultato dipende dalla capacità del modello AI di interpretare l'immagine originale.
- È necessaria una connessione a Internet attiva per contattare l'API di Gemini.
- Lo script gestisce gli errori di base, come percorsi file non validi o chiavi API vuote.
