## _Esportazione Struttura Cartelle Interattiva_ - **tree_size.py** 🌳

Uno script Python che scansiona ricorsivamente una directory (locale o di rete) e genera un **file HTML interattivo** con la struttura completa di cartelle e file, navigabile offline come in “Esplora Risorse” di Windows.

---

### Descrizione 📄

L'**Esportazione Struttura Cartelle Interattiva** permette di catturare una vera e propria “fotografia” della gerarchia di una directory fornita dall’utente. Lo script rileva tutte le sottocartelle e i file, raccogliendo informazioni come:

- Nome della cartella o del file
- Data di creazione
- Dimensione leggibile (KB, MB, GB)

Il risultato viene salvato in un **file HTML autocontenuto**, compatibile con qualsiasi dispositivo e consultabile anche se il disco originale non è più disponibile.

Utile per:

- **Consultazione offline** di strutture complesse.
- **Analisi e report** di directory aziendali o di rete.
- **Documentazione e backup** della gerarchia di file.

---

### Funzionalità 🌟

- **Scansione ricorsiva completa**: Analizza tutte le sottocartelle e i file fino alla massima profondità.
- **Supporto UNC Windows**: Gestisce condivisioni di rete richiedendo credenziali se necessario.
- **Albero interattivo**: Struttura HTML espandibile e collassabile, stile Esplora Risorse.
- **Filtro ricerca per nome**: Cerca file e cartelle per nome senza considerare data o dimensione.
- **Output offline e sicuro**: File HTML autocontenuto, con CSS e JavaScript inline, senza collegamenti esterni.
- **Compatibilità multi-OS**: Funziona su Windows, Linux e macOS.
- **Dimensioni leggibili**: File e cartelle mostrano dimensione in formato comprensibile (KB, MB, GB).
- **Date di creazione**: Mostra la data di creazione o ultima modifica dei file e delle cartelle.

---

#### Esempio Input

```plaintext
Inserisci il percorso: \\server\share\cartella
```

Lo script analizzerà il percorso inserito (locale o di rete) e genererà un file HTML interattivo della struttura completa.

---

### Output 📊

#### Output Terminale

```plaintext
Esportazione completata: Export_data_2025-08-29.html
```

#### Contenuto del File di Output

- Struttura ad albero espandibile/chiudibile
- Nome di file e cartelle
- Data di creazione
- Dimensione leggibile
- Filtro di ricerca per nome (solo nome, senza considerare data o dimensione)

Esempio di visualizzazione:

```
▸ Cartella1
    ▸ SottocartellaA
        file1.txt  12 KB  2025-08-29 10:30
    ▸ SottocartellaB
        file2.pdf  234 KB  2025-08-28 09:15
▸ Cartella2
    file3.docx  1.2 MB  2025-08-27 14:20
```

---

### Note 📝

- **Percorsi validi**: Verifica che il percorso inserito esista e sia accessibile. Su Windows, lo script può richiedere **utente e password** per accesso a condivisioni di rete UNC.
- **Output non distruttivo**: Lo script non modifica o elimina alcun file o cartella.
- **Compatibilità offline**: Il file HTML può essere aperto senza collegamento alla directory originale.
- <del>**Filtro ricerca**: La ricerca agisce solo sui **nomi di file e cartelle**, ignorando data e dimensione.</del> **Attualmente con Bug**
