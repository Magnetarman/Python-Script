<p align="center">
	<img src="https://raw.githubusercontent.com/Magnetarman/Python-Script/refs/heads/main/Banner.png" alt="python-script-banner" width="800">
</p>
<br>
<p align="center">
	<em><code>Script Python Utili. Gli script sono testati personalmente ed utilizzati giornalmente.</code></em>
</p>
<br>
<p align="center">
	<img src="https://img.shields.io/badge/version-3.3-green.svg" alt="versione">
	<img src="https://img.shields.io/github/last-commit/Magnetarman/Python-Script?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Magnetarman/Python-Script?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Magnetarman/Python-Script?style=flat&color=0080ff" alt="repo-language-count">
	<img src="https://img.shields.io/github/license/Magnetarman/Python-Script?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
  <img src="https://github.com/Magnetarman/Python-Script/actions/workflows/update-reqs.yml/badge.svg" alt="requirements.txt">
</p>
<p align="center">Tool e Tecnologie Utilizzate:</p>
<p align="center">
	<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/PowerShell-5391FE.svg?style=flat&logo=PowerShell&logoColor=white" alt="PowerShell">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
</p>
<hr>

## 👾 Features

**Versione 3.0** - Nuovo approccio all'esecuzione: non si esegue più uno script isolato, ma tramite un unico punto d’ingresso interattivo.

> Introdotto il file `main.py` che gestisce:
>
> - L'installazione automatica delle dipendenze dal file `requirements.txt`.
> - Un menu interattivo per scegliere quale script eseguire.
> - Organizzazione automatica degli script in ordine alfabetico.
> - Breve descrizione affiancata a ciascuno script.
> - Migliore gestione e chiarezza degli strumenti disponibili.

---

## 📁 Struttura Cartelle

```sh
└── Python-Script
    ├── .github
    │   └── workflows
    │       └── update-reqs.yml
    ├── LICENSE
    ├── README.md
    ├── install.ps1
    ├── main.py
    └── Docs
        ├── audio_extract.md
        ├── codec_expoler.md
        ├── color_palette.md
        ├── efolder.md
        ├── eml_converter.md
        ├── estensioni.md
        ├── image_downloader.md
        ├── png_converter.md
        ├── remove.md
        ├── sposta_file.md
        ├── transcribe_wav.md
        ├── pdf_combiner.md
        ├── trash.md
        └── tree_size.md
    ├── pipreqs-config.toml
    ├── requirements.txt
    └── scripts
        ├── audio_extract.py
        ├── codec_expoler.py
        ├── color_palette.py
        ├── efolder.py
        ├── eml_converter.py
        ├── estensioni.py
        ├── image_downloader.py
        ├── png_converter.py
        ├── remove.py
        ├── sposta_file.py
        ├── transcribe_wav.py
        ├── pdf_combiner.py
        ├── trash.py
        └── tree_size.py
```

### 📂 Index Progetto

<details open>
	<summary><b><code>PYTHON-SCRIPT</code></b></summary>
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/install.ps1'>install.ps1</a></b></td>
					<td><code>❯ Installa Python 3.10 e lancia lo script generale "main.py"</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/main.py'>main.py</a></b></td>
					<td><code>❯ Script Generale con breve descrizione degli script disponibili</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td><code>❯ Librerie necessarie al funzionamento degli script</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<details>
		<summary><b>Docs</b></summary>
		<blockquote>
			<table>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/audio_extract.md'>audio_extract.py</a></b></td>
					<td><code>❯ Estrazione tracce audio .flac da file .mkv (anche ricorsiva).</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/codec_explorer.md'>codec_expoler.py</a></b></td>
					<td><code>❯ Analizza i file video identifica codec H264 o H265, ne mostra i dettagli e consente l’esportazione.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/color_palette.md'>color_palette.py</a></b></td>
					<td><code>❯ Estrazione e salvataggio dei colori in formato PDF dominanti da un'immagine.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/efolder.md'>efolder.py</a></b></td>
					<td><code>❯ Individuazione e rimozione sicura di cartelle vuote in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/eml_converter.md'>eml_converter.py</a></b></td>
					<td><code>❯ Conversione di email .eml in PDF con dettagli del messaggio.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/estensioni.md'>estensioni.py</a></b></td>
					<td><code>❯ Analisi e elenco ordinato delle estensioni file in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/image_downloader.md'>image_downloader.py</a></b></td>
					<td><code>❯ Download immagini da una pagina web, inclusi contenuti Base64.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/pdf_combiner.md'>pdf_combiner.py</a></b></td>
					<td><code>❯  Genera PDF da immagini Jpeg.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/png_converter.md'>png_converter.py</a></b></td>
					<td><code>❯ Conversione ricorsiva di tutte le immagini PNG in JPEG all'interno di una cartella specificata, gestendo la trasparenza e rimuovendo i file PNG originali.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/remove.md'>remove.py</a></b></td>
					<td><code>❯ Rimozione file non musicali e pulizia cartelle vuote in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/sposta_file.md'>sposta_file.py</a></b></td>
					<td><code>❯ Spostamento file in directory principale e rimozione cartelle vuote.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/transcribe_wav.md'>transcribe_wav.py</a></b></td>
					<td><code>❯ Trascrive automaticamente i file audio .wav in testo utilizzando il modello Whisper, salvando le trascrizioni e saltando quelle già esistenti.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/trash.md'>trash.py</a></b></td>
					<td><code>❯ Spostamento file con nomi specifici in una cartella "duplicati".</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/main/Docs/tree_size.md'>tree_size.py</a></b></td>
					<td><code>❯ Esporta la "fotografia" completa e interattiva di una struttura di cartelle in un file HTML statico.</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<details>
		<summary><b>scripts</b></summary>
		<blockquote>
			<table>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/audio_extract.py'>audio_extract.py</a></b></td>
					<td><code>❯ Estrazione tracce audio .flac da file .mkv (anche ricorsiva).</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/codec_expoler.py'>codec_expoler.py</a></b></td>
					<td><code>❯ Analizza i file video identifica codec H264 o H265, ne mostra i dettagli e consente l’esportazione.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/color_palette.py'>color_palette.py</a></b></td>
					<td><code>❯ Estrazione e salvataggio dei colori in formato PDF dominanti da un'immagine.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/efolder.py'>efolder.py</a></b></td>
					<td><code>❯ Individuazione e rimozione sicura di cartelle vuote in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/eml_converter.py'>eml_converter.py</a></b></td>
					<td><code>❯ Conversione di email .eml in PDF con dettagli del messaggio.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/estensioni.py'>estensioni.py</a></b></td>
					<td><code>❯ Analisi e elenco ordinato delle estensioni file in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/image_downloader.py'>image_downloader.py</a></b></td>
					<td><code>❯ Download immagini da una pagina web, inclusi contenuti Base64.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/pdf_combiner.py'>pdf_combiner.py</a></b></td>
					<td><code>❯  Genera PDF da immagini Jpeg.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/png_converter.py'>png_converter.py</a></b></td>
					<td><code>❯ Conversione ricorsiva di tutte le immagini PNG in JPEG all'interno di una cartella specificata, gestendo la trasparenza e rimuovendo i file PNG originali.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/remove.py'>remove.py</a></b></td>
					<td><code>❯ Rimozione file non musicali e pulizia cartelle vuote in una directory.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/sposta_file.py'>sposta_file.py</a></b></td>
					<td><code>❯ Spostamento file in directory principale e rimozione cartelle vuote.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/transcribe_wav.py'>transcribe_wav.py</a></b></td>
					<td><code>❯ Trascrive automaticamente i file audio .wav in testo utilizzando il modello Whisper, salvando le trascrizioni e saltando quelle già esistenti.</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/trash.py'>trash.py</a></b></td>
					<td><code>❯ Spostamento file con nomi specifici in una cartella "duplicati".</code></td>
				</tr>
				<tr>
					<td><b><a href='https://github.com/Magnetarman/Python-Script/blob/master/scripts/tree_size.py'>tree_size.py</a></b></td>
					<td><code>❯ Esporta la "fotografia" completa e interattiva di una struttura di cartelle in un file HTML statico.</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## 🚀 Getting Started

### ☑️ Prerequisiti

Prima di iniziare con Python-Script, assicurati che il tuo ambiente di esecuzione soddisfi i seguenti requisiti:

- **Linguaggio di Programmazione:** Python
- **Gestore di Pacchetti:** Pip

### ⚙️ Installatione

Utilizza Python-Script seguendo questi step:

1. Clona la repository the Python-Script:

```sh
❯ git clone https://github.com/Magnetarman/Python-Script
```

2. Utilizza il terminale per Navigare fino alla cartella:

```sh
❯ cd Python-Script
```

3. Lancia "main.py":

```sh
❯ py main.py
```

### ⚙️ Installatione Alternativa

1. Clona la repository the Python-Script:

```sh
❯ git clone https://github.com/Magnetarman/Python-Script
```

2. Avvia il terminale in **modalita amministratore**, Naviga fino alla cartella:

```sh
❯ cd Python-Script
```

3. Avvia lo script `install.ps1`:

```sh
❯ ./install.ps1
```

> Lo script `install.ps1` avviato installerà Python e dipendenze minimali. Successivamente lo scipt si occuperà di avviare automaticamente il `main.py` per utilizzare gli script disponibili.

---

## 📌 Roadmap

- [x] **`V 3.0`**: <strike>Creazione 'main.py'.</strike>
- [x] **`V 3.1`**: <strike>Refactor 'Readme.md'. Creazione Cartella 'Docs' con la documentazione di ogni script.</strike>
- [x] **`V 3.1.1`**: <strike>Aggiunta Script PDF Combiner in versione Stabile.</strike>
- [x] **`V 3.1.2`**: <strike>il wrapper `main.py` aggiunge automaticamente i nuovi script all'avvio.</strike>
- [x] **`V 3.2`**: <strike>Automatizzare il processo di installazione di Python e dipendenze al 100%.</strike>
- [x] **`V 3.3`**: Aggiunti nuovi script, aggiunta documentazione mancante. 'main.py' non viene terminato alla fine di uno script.
- [ ] **`V 4.0`**: unificare il tutto in un unico 'main.py' con aggiunta di Interfaccia grafica.

---

## 🔰 Come Contribuire

- **💬 [Partecipa alle Discussioni](https://t.me/GlitchTalkGroup)**: Condividi le tue idee, fornisci feedback o fai domande.
- **🐛 [Segnala Problemi](https://github.com/Magnetarman/Python-Script/issues)**: Segnala i bug trovati o richiedi nuove funzionalità per il progetto \Python-Script`.
- **💡 [ Invia Pull Request](https://github.com/Magnetarman/Python-Script/blob/main/CONTRIBUTING.md)**: Revisiona le Pull Request (PR) aperte e invia le tue.

<br>
<details closed>
<summary>📖 Linee Guida </summary>

1. **Esegui il Fork della Repository**: Inizia facendo il "fork" della repository del progetto sul tuo account GitHub.
2. **Clona in Locale**: Clona la repository di cui hai fatto il fork sulla tua macchina locale usando un client Git.
   ```sh
   git clone https://github.com/Magnetarman/Python-Script
   ```
3. **Crea un Nuovo Branch**: Lavora sempre su un nuovo "branch", dandogli un nome descrittivo.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Apporta le Tue Modifiche**: Sviluppa e testa le tue modifiche in locale.
5. **Esegui il Commit delle Tue Modifiche**: Fai il "commit" con un messaggio chiaro che descriva i tuoi aggiornamenti.
   ```sh
   git commit -m 'Implementata nuova funzionalità x.'
   ```
6. **Esegui il Push su GitHub**: Fai il "push" delle modifiche sulla tua repository "fork".
   ```sh
   git push origin nuova-funzionalita-x
   ```
7. **Invia una Pull Request**: Crea una "Pull Request" (PR) verso la repository originale del progetto. Descrivi chiaramente le modifiche e le loro motivazioni.
8. **Revisione**: Una volta che la tua PR sarà revisionata e approvata, verrà unita ("merged") nel branch principale. Congratulazioni per il tuo contributo!
</details>

---

## 🎗 Licenza

Creato con ❤️ da [Magnetarman](https://magnetarman.com/), potenziato da ChatGPT e grazie ad [Antonio Porcelli](https://progressify.dev/) per avermi inizializzato allo scrivere e capire Python. Licenza MIT.

---
