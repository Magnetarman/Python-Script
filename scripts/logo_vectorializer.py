# script Python per vettorializzare loghi da file immagine tramite Google Gemini.

import os
import sys
from pathlib import Path

# È necessario installare la libreria: pip install google-generativeai
try:
    import google.generativeai as genai
except ImportError:
    print("Errore: La libreria 'google-generativeai' non è installata.")
    print("Per favore, installala eseguendo: pip install google-generativeai")
    sys.exit(1)

def get_and_validate_file_path():
    """
    Chiede all'utente di inserire il percorso di un file immagine e ne valida
    l'esistenza e il formato (.png, .jpeg, .svg).

    In caso di input non valido, il programma termina.

    Returns:
        pathlib.Path: Un oggetto Path che rappresenta il file immagine valido.
    """
    file_path_str = input("Inserisci il percorso del file immagine (png, jpeg, svg): ")

    # Controlla che il percorso non sia vuoto
    if not file_path_str:
        print("Errore: Il percorso del file non può essere vuoto.")
        return None

    file_path = Path(file_path_str.strip())

    # Verifica l'esistenza del file
    if not file_path.is_file():
        print(f"Errore: Il file '{file_path}' non è stato trovato.")
        return None

    # Controlla che il formato sia tra quelli supportati
    supported_formats = ['.png', '.jpeg', '.jpg', '.svg']
    if file_path.suffix.lower() not in supported_formats:
        print(f"Errore: Formato file non supportato. Usa uno dei seguenti: {', '.join(supported_formats)}")
        return None

    return file_path

def get_gemini_api_key():
    """
    Chiede all'utente di inserire il proprio token API di Google Gemini
    e verifica che non sia vuoto.

    Returns:
        str: La chiave API fornita dall'utente.
    """
    api_key = input("Inserisci il tuo Google Gemini API token key: ")

    # Verifica che la chiave non sia una stringa vuota
    if not api_key or not api_key.strip():
        print("Errore: Il token API non può essere vuoto.")
        return None

    return api_key.strip()

def call_gemini_api(api_key, image_path):
    """
    Configura l'API di Gemini, carica l'immagine e invia la richiesta
    per la vettorializzazione.

    Args:
        api_key (str): La chiave API di Google Gemini.
        image_path (pathlib.Path): Il percorso del file immagine da elaborare.

    Returns:
        str: Il contenuto SVG generato come stringa, oppure None in caso di errore.
    """
    try:
        # Configura il client dell'API con la chiave fornita
        genai.configure(api_key=api_key)

        print("Caricamento dell'immagine...")
        # Carica il file immagine per renderlo disponibile all'API
        uploaded_image = genai.upload_file(path=str(image_path))

        # Inizializza il modello generativo
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

        # Definisce il prompt per la richiesta di vettorializzazione
        prompt = (
            "Analizza attentamente questa immagine. Ricrea un logo in formato .svg vettoriale, "
            "senza sfondo, che sia pixel-perfect ed esteticamente identico all’originale. "
            "L’obiettivo è ottenere un file finale utilizzabile come logo ufficiale in qualsiasi contesto grafico. "
            "L'output deve contenere ESCLUSIVAMENTE il codice SVG, senza alcuna formattazione "
            "aggiuntiva come '```svg', spiegazioni o commenti."
        )

        print("Invio dell’immagine a Google Gemini in corso...")
        print("Attesa della risposta (l'operazione potrebbe richiedere alcuni istanti)...")

        # Invia la richiesta all'API combinando il prompt testuale e l'immagine
        response = model.generate_content([prompt, uploaded_image])

        # Pulisce la risposta per estrarre solo il codice SVG
        svg_content = response.text.strip()
        if svg_content.startswith("```svg"):
            svg_content = svg_content[5:]
        if svg_content.endswith("```"):
            svg_content = svg_content[:-3]

        return svg_content.strip()

    except Exception as e:
        print(f"Errore durante la comunicazione con l'API Gemini: {e}")
        return None

def save_output_file(original_path, svg_content):
    """
    Salva il contenuto SVG in un nuovo file nella stessa cartella dello script.

    Args:
        original_path (pathlib.Path): Il percorso del file immagine originale.
        svg_content (str): La stringa contenente il codice SVG da salvare.

    Returns:
        str: Il percorso completo del file di output salvato, o None se si verifica un errore.
    """
    try:
        # Costruisce il nome del file di output partendo dall'originale
        output_filename = f"{original_path.stem}-Vector.svg"

        # Determina la directory in cui si trova lo script in esecuzione
        script_directory = Path(sys.argv[0]).parent
        output_path = script_directory / output_filename

        print(f"Salvataggio del file in corso: {output_path}")

        # Scrive il contenuto SVG nel file di destinazione
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return str(output_path)

    except IOError as e:
        print(f"Errore durante il salvataggio del file su disco: {e}")
        return None

def main():
    """
    Funzione principale che orchestra l'intero processo:
    1. Richiede e valida gli input dell'utente.
    2. Chiama l'API per l'elaborazione.
    3. Salva il risultato.
    4. Comunica l'esito finale.
    """
    print("--- Logo Vectorializer con Google Gemini ---")

    # Fase 1: Input e validazione del percorso del file
    image_path = get_and_validate_file_path()
    if not image_path:
        print("\nProgramma terminato a causa di un input non valido.")
        sys.exit(1)  # Termina l'esecuzione con un codice di errore

    # Fase 2: Input e validazione della chiave API
    api_key = get_gemini_api_key()
    if not api_key:
        print("\nProgramma terminato a causa di un input non valido.")
        sys.exit(1)

    # Fase 3: Elaborazione tramite API Gemini
    svg_result = call_gemini_api(api_key, image_path)
    if not svg_result:
        print("\nElaborazione fallita. Il programma verrà terminato.")
        sys.exit(1)

    # Fase 4: Salvataggio del file di output
    saved_file_path = save_output_file(image_path, svg_result)

    # Fase 5: Comunicazione dell'esito finale
    print("-" * 30)
    if saved_file_path:
        print("✅ Esito finale: SUCCESSO")
        print(f"Logo vettoriale generato con successo: {saved_file_path}")
    else:
        print("❌ Esito finale: ERRORE")
        print("Si è verificato un errore durante il salvataggio del file.")
    print("-" * 30)


if __name__ == "__main__":
    main()