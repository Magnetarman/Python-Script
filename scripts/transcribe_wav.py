#!/usr/bin/env python3
import os
import subprocess
import sys
import importlib

def upgrade_pip_and_install_whisper():
    """
    Aggiorna pip e installa o reinstalla correttamente whisper.
    """
    user_name = os.getlogin()
    python_path = os.path.join(f"C:\\Users\\{user_name}\\AppData\\Local\\Programs\\Python\\Python310", "python.exe")
    
    if not os.path.exists(python_path):
        print(f"Errore: Python 3.10 non trovato in {python_path}.")
        sys.exit(1)
    
    print("Aggiornamento di pip in corso...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'aggiornamento di pip: {e}")
        sys.exit(1)
    
    print("Disinstallazione di vecchie versioni di whisper...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "uninstall", "whisper", "-y"])
    except subprocess.CalledProcessError:
        # Ignora errori se whisper non è installato
        pass
    
    print("Installazione di openai-whisper...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "-U", "openai-whisper"])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione di openai-whisper: {e}")
        sys.exit(1)

def ensure_python_3_10():
    """
    Verifica se Python 3.10 è in uso, altrimenti forza l'esecuzione con Python 3.10.
    """
    if sys.version_info[0] != 3 or sys.version_info[1] != 10:
        print("Forzando l'esecuzione con Python 3.10...")

        # Recupera il nome dell'utente corrente
        user_name = os.getlogin()

        # Costruisci il percorso di Python 3.10 dinamicamente
        python_path = os.path.join(f"C:\\Users\\{user_name}\\AppData\\Local\\Programs\\Python\\Python310", "python.exe")

        if not os.path.exists(python_path):
            print(f"Errore: Python 3.10 non trovato in {python_path}. Verifica che Python 3.10 sia installato correttamente.")
            sys.exit(1)
        
        # Verifica se python3.10 è disponibile
        try:
            subprocess.check_call([python_path, "--version"])
        except subprocess.CalledProcessError:
            print("Errore: Python 3.10 non trovato o non configurato correttamente.")
            sys.exit(1)
        
        # Esegui lo script con Python 3.10
        subprocess.check_call([python_path, os.path.abspath(__file__)] + sys.argv[1:])
        sys.exit()  # Termina il processo attuale, in modo che non venga eseguito altro codice

def import_whisper():
    """
    Importa il modulo whisper in modo sicuro.
    """
    try:
        import whisper
        return whisper
    except ImportError:
        print("Modulo whisper non trovato. Installazione in corso...")
        upgrade_pip_and_install_whisper()
        # Riprova ad importare dopo l'installazione
        try:
            import whisper
            return whisper
        except ImportError as e:
            print(f"Impossibile importare whisper anche dopo l'installazione: {e}")
            sys.exit(1)

def transcribe_podcast(file_path, model_name='medium', language='it'):
    """
    Trascrive un file audio in formato .wav utilizzando il modello Whisper.
    """
    whisper = import_whisper()
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path, language=language)
    return result['text']

def save_transcription(transcription, output_path):
    """
    Salva la trascrizione in un file di testo.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

def main(podcast_dir):
    for root, dirs, files in os.walk(podcast_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            base_name, ext = os.path.splitext(file_name)

            # Supportati formati audio (solo .wav ora)
            if ext.lower() == '.wav':
                output_file_name = base_name + '.txt'
                output_path = os.path.join(root, output_file_name)

                # Verifica se la trascrizione esiste già
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1:
                    print(f'Saltato {file_name}, il file di trascrizione esiste già.')
                    continue

                try:
                    print(f'Trascrizione in corso per {file_name}...')
                    transcription = transcribe_podcast(file_path)
                    save_transcription(transcription, output_path)
                    print(f'Trascrizione completata per {file_name}, salvata in {output_path}')
                except Exception as e:
                    print(f'Errore durante la trascrizione di {file_name}: {e}')

if __name__ == "__main__":
    # Verifica che Python 3.10 sia utilizzato
    ensure_python_3_10()
    
    # Aggiorna pip e installa correttamente whisper
    upgrade_pip_and_install_whisper()

    podcast_dir = input("Inserisci il percorso della cartella contenente i podcast: ").strip()
    if os.path.isdir(podcast_dir):
        main(podcast_dir)
        print("Trascrizione completata.")
    else:
        print("Il percorso inserito non è valido. Per favore riprova.")