## _Trascrizione Automatica Podcast_ - **transcribe_wav.py** 🎙️

Uno script Python che trascrive automaticamente i file audio in formato **.wav** in testo utilizzando il modello Whisper di OpenAI, salvando le trascrizioni e saltando quelle già presenti.

---

### Descrizione 📄

Il progetto **Trascrizione Automatica Podcast** permette di convertire facilmente registrazioni audio in testo leggibile. Lo script verifica se la trascrizione esiste già per ogni file e, se non presente, utilizza il modello Whisper per generarla. Il risultato viene salvato come file di testo nella stessa cartella dell'audio originale.

Utile per:

- **Trascrivere contenuti audio** di podcast o interviste.
- **Creare archivi testuali** di registrazioni audio.
- **Risparmiare tempo** evitando di trascrivere manualmente.

---

### Funzionalità 🌟

- **Supporto Python 3.10**: Verifica e forza l'esecuzione con Python 3.10 se necessario.
- **Installazione automatica di Whisper**: Aggiorna pip e installa (o reinstalla) openai-whisper se non presente.
- **Trascrizione automatica**: Analizza i file .wav presenti nella cartella specificata.
- **Skip file già trascritti**: Salta i file che hanno già una trascrizione esistente.
- **Salvataggio sicuro**: Le trascrizioni vengono salvate come file .txt nella stessa cartella dell'audio.
- **Gestione errori**: Notifica eventuali errori durante la trascrizione senza interrompere l'esecuzione.

---

#### Esempio Input

```plaintext
Inserisci il percorso della cartella contenente i podcast: C:\Users\User\Podcasts
```

Lo script analizzerà tutti i file .wav nella cartella e sottocartelle e genererà i file di trascrizione corrispondenti.

---

### Output 📊

#### Output Terminale

```plaintext
Trascrizione in corso per episodio1.wav...
Trascrizione completata per episodio1.wav, salvata in C:\Users\User\Podcasts\episodio1.txt
Saltato episodio2.wav, il file di trascrizione esiste già.
Trascrizione completata.
```

#### Contenuto del File di Output

- Trascrizione testuale del contenuto audio.
- File salvato nella stessa cartella dell'audio con estensione .txt.

Esempio di visualizzazione:

```plaintext
Ciao a tutti e benvenuti al nostro podcast.
Oggi parleremo di tecnologia e innovazione...
```

---

### Note 📝

- **Percorsi validi**: Verifica che la cartella inserita esista.
- **Formati supportati**: Attualmente lo script gestisce solo file **.wav**.
- **Compatibilità**: Assicurarsi di avere Python 3.10 installato.
- **Output non distruttivo**: Lo script non modifica i file audio originali.
- **Installazione automatica**: Pip e Whisper vengono aggiornati/installati automaticamente se necessario.
