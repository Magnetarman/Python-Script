## _Trascrizione Automatica Podcast_ - **transcribe_wav.py** 🎙️

Uno script Python che trascrive automaticamente file audio in vari formati (WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4) in testo utilizzando il modello Whisper di OpenAI. Converte automaticamente i formati non-WAV in WAV per la trascrizione, salvando le trascrizioni e saltando quelle già presenti.

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
- **Conversione automatica formati**: Converte automaticamente MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4 in WAV utilizzando FFmpeg.
- **Accelerazione audio 2x**: Opzionalmente accelera l'audio a 2x velocità utilizzando FFmpeg per velocizzare la trascrizione.
- **Trascrizione automatica**: Analizza tutti i file audio supportati presenti nella cartella specificata.
- **Skip file già trascritti**: Salta i file che hanno già una trascrizione esistente.
- **Salvataggio sicuro**: Le trascrizioni vengono salvate come file .txt nella stessa cartella dell'audio.
- **Gestione errori**: Notifica eventuali errori durante la trascrizione senza interrompere l'esecuzione.
- **Pulizia automatica**: Rimuove automaticamente i file temporanei creati durante l'accelerazione e conversione.

---

#### Esempio Input

```plaintext
Inserisci il percorso della cartella contenente i podcast: C:\Users\User\Podcasts
```

Lo script analizzerà tutti i file audio supportati nella cartella e sottocartelle e genererà i file di trascrizione corrispondenti.

---

### Conversione Automatica Formati 🔄

Lo script supporta automaticamente la conversione di vari formati audio in WAV per la trascrizione:

- **Formati supportati**: WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4
- **Conversione automatica**: I formati non-WAV vengono convertiti automaticamente utilizzando FFmpeg
- **Qualità preservata**: La conversione mantiene la qualità audio originale
- **Processo trasparente**: Conversione e pulizia automatica dei file temporanei
- **Fallback intelligente**: Se la conversione fallisce, il file viene saltato con messaggio di errore

**Esempio di conversione durante l'esecuzione:**

```plaintext
Conversione da MP3 a WAV richiesta...
Conversione in corso: podcast.mp3 → WAV
Conversione completata: podcast_converted.wav
Trascrizione in corso per podcast.mp3...
File WAV convertito rimosso
Trascrizione completata per podcast.mp3, salvata in podcast.txt
```

---

### Esempio Input con Conversione e Accelerazione 2x

```plaintext
Inserisci il percorso della cartella contenente i podcast: C:\Users\User\Podcasts
Vuoi accelerare l'audio a 2x velocità per velocizzare la trascrizione? (s/n): s
Modalità velocità 2x attivata
Conversione da MP3 a WAV richiesta...
Conversione in corso: episodio1.mp3 → WAV
Conversione completata: episodio1_converted.wav
Accelerazione audio 2x in corso...
Audio accelerato 2x: episodio1_converted.wav
Audio accelerato con successo
Trascrizione in corso per episodio1.mp3...
File temporaneo rimosso
File WAV convertito rimosso
Trascrizione completata per episodio1.mp3, salvata in C:\Users\User\Podcasts\episodio1.txt
```

---

### Accelerazione Audio 2x ⚡

La nuova funzionalità di accelerazione audio permette di velocizzare significativamente il processo di trascrizione:

- **Come funziona**: Utilizza FFmpeg per accelerare l'audio a 2x velocità mantenendo il pitch originale
- **Vantaggi**: Riduce i tempi di elaborazione di circa il 50% mantenendo la qualità della trascrizione
- **Requisiti**: Richiede FFmpeg installato nel sistema
- **Processo automatico**: Crea file temporanei accelerati, li trascrive e li elimina automaticamente
- **Fallback sicuro**: Se l'accelerazione fallisce, utilizza il file originale

**Nota**: L'accelerazione audio è opzionale e può essere abilitata/disabilitata ad ogni esecuzione.

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
- **Formati supportati**: WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4.
- **Conversione automatica**: I formati non-WAV vengono convertiti automaticamente in WAV per la trascrizione.
- **Compatibilità**: Assicurarsi di avere Python 3.10 installato.
- **Output non distruttivo**: Lo script non modifica i file audio originali.
- **Installazione automatica**: Pip e Whisper vengono aggiornati/installati automaticamente se necessario.
- **FFmpeg richiesto**: Per la conversione formati e accelerazione 2x, installa FFmpeg nel sistema.
