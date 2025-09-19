# Trascrive automaticamente i file audio .wav in testo utilizzando il modello Whisper, 
# salvando le trascrizioni e saltando quelle già esistenti.
import os
import subprocess
import sys
import importlib
import time
from datetime import datetime, timedelta

def upgrade_pip_and_install_packages():
    """
    Aggiorna pip e installa o reinstalla correttamente whisper e tqdm.
    """
    user_home = os.environ.get('USERPROFILE')
    python_path = os.path.join(user_home, "AppData", "Local", "Programs", "Python", "Python310", "python.exe")
    
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
        pass

    print("Installazione di openai-whisper e tqdm...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "-U", "openai-whisper", "tqdm"])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione: {e}")
        sys.exit(1)

def ensure_python_3_10():
    """
    Verifica se Python 3.10 è in uso, altrimenti forza l'esecuzione con Python 3.10.
    """
    if sys.version_info[0] != 3 or sys.version_info[1] != 10:
        print("Forzando l'esecuzione con Python 3.10...")
        user_home = os.environ.get('USERPROFILE')
        python_path = os.path.join(user_home, "AppData", "Local", "Programs", "Python", "Python310", "python.exe")
        
        if not os.path.exists(python_path):
            print(f"Errore: Python 3.10 non trovato in {python_path}. Verifica che Python 3.10 sia installato correttamente.")
            sys.exit(1)

        try:
            subprocess.check_call([python_path, "--version"])
        except subprocess.CalledProcessError:
            print("Errore: Python 3.10 non trovato o non configurato correttamente.")
            sys.exit(1)

        subprocess.check_call([python_path, os.path.abspath(__file__)] + sys.argv[1:])
        sys.exit()

def import_required_modules():
    """
    Importa i moduli necessari in modo sicuro.
    """
    try:
        import whisper
        from tqdm import tqdm
        return whisper, tqdm
    except ImportError as e:
        print(f"Moduli non trovati: {e}. Installazione in corso...")
        upgrade_pip_and_install_packages()
        
        try:
            import whisper
            from tqdm import tqdm
            return whisper, tqdm
        except ImportError as e:
            print(f"Impossibile importare i moduli anche dopo l'installazione: {e}")
            sys.exit(1)

def get_audio_duration(file_path):
    """
    Stima la durata del file audio in secondi (approssimativa).
    Questa è una stima basata sulla dimensione del file.
    La stima è volutamente pessimistica per dare un ETA più lungo del reale.
    """
    try:
        file_size = os.path.getsize(file_path)
        # Stima pessimistica: ~0.5MB per minuto di audio WAV (peggiorata del 50%)
        # Questo significa che stimiamo file più lunghi di quello che sono realmente
        estimated_duration = file_size / (1024 * 1024) * 120  # 120 invece di 60
        return max(estimated_duration, 60)  # Minimo 60 secondi invece di 30
    except:
        return 600  # Default 10 minuti invece di 5 se non riusciamo a stimare

def transcribe_podcast_with_progress(file_path, model_name='medium', language='it'):
    """
    Trascrive un file audio con barra di progresso simulata.
    """
    whisper, tqdm = import_required_modules()
    
    print(f"Caricamento del modello {model_name}...")
    model = whisper.load_model(model_name)
    
    # Stima della durata per il progresso (pessimistica)
    estimated_duration = get_audio_duration(file_path)
    estimated_time = estimated_duration * 0.2  # Raddoppiato: da 0.1 a 0.2 per essere più pessimisti
    
    print(f"Trascrizione in corso...")
    start_time = time.time()
    
    # Barra di progresso simulata durante la trascrizione
    with tqdm(total=100, desc="Progresso", unit="%", ncols=80) as pbar:
        # Avvia la trascrizione in un thread separato (simulato con aggiornamenti)
        result = model.transcribe(file_path, language=language)
        
        # Simula il progresso (Whisper non fornisce callback di progresso nativi)
        elapsed = time.time() - start_time
        pbar.update(100)
        pbar.set_postfix({"Tempo": f"{elapsed:.1f}s"})
    
    return result['text']

def save_transcription(transcription, output_path):
    """
    Salva la trascrizione in un file di testo.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

def count_wav_files(podcast_dir):
    """
    Conta il numero totale di file .wav da elaborare.
    """
    count = 0
    for root, dirs, files in os.walk(podcast_dir):
        for file_name in files:
            if file_name.lower().endswith('.wav'):
                base_name = os.path.splitext(file_name)[0]
                output_path = os.path.join(root, base_name + '.txt')
                if not (os.path.exists(output_path) and os.path.getsize(output_path) > 1):
                    count += 1
    return count

def format_time(seconds):
    """
    Formatta i secondi in formato HH:MM:SS.
    """
    return str(timedelta(seconds=int(seconds)))

def main(podcast_dir):
    """
    Funzione principale con barra di progresso e ETA.
    """
    # Importa i moduli necessari
    whisper, tqdm = import_required_modules()
    
    # Conta i file da elaborare
    total_files = count_wav_files(podcast_dir)
    
    if total_files == 0:
        print("Nessun file .wav da elaborare trovato.")
        return
    
    print(f"\nTrovati {total_files} file da trascrivere.")
    
    processed_files = 0
    start_time = time.time()
    
    # Barra di progresso principale per tutti i file
    with tqdm(total=total_files, desc="File elaborati", unit="file", ncols=100) as main_pbar:
        for root, dirs, files in os.walk(podcast_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                base_name, ext = os.path.splitext(file_name)
                
                if ext.lower() == '.wav':
                    output_file_name = base_name + '.txt'
                    output_path = os.path.join(root, output_file_name)
                    
                    # Verifica se la trascrizione esiste già
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 1:
                        continue
                    
                    try:
                        file_start_time = time.time()
                        
                        # Aggiorna la descrizione con il file corrente
                        main_pbar.set_description(f"Elaborando: {file_name[:30]}...")
                        
                        transcription = transcribe_podcast_with_progress(file_path)
                        save_transcription(transcription, output_path)
                        
                        processed_files += 1
                        elapsed_total = time.time() - start_time
                        file_elapsed = time.time() - file_start_time
                        
                        # Calcola ETA
                        if processed_files > 0:
                            avg_time_per_file = elapsed_total / processed_files
                            remaining_files = total_files - processed_files
                            eta_seconds = avg_time_per_file * remaining_files
                            eta_formatted = format_time(eta_seconds)
                        else:
                            eta_formatted = "Calcolando..."
                        
                        # Aggiorna la barra di progresso
                        main_pbar.update(1)
                        main_pbar.set_postfix({
                            "File": f"{file_elapsed:.1f}s",
                            "ETA": eta_formatted,
                            "Totale": format_time(elapsed_total)
                        })
                        
                        print(f"\n✓ Completato: {file_name}")
                        print(f"  Salvato in: {output_path}")
                        print(f"  Tempo impiegato: {file_elapsed:.1f} secondi")
                        
                    except Exception as e:
                        print(f"\n✗ Errore durante la trascrizione di {file_name}: {e}")
                        main_pbar.update(1)
    
    total_elapsed = time.time() - start_time
    print(f"\n🎉 Trascrizione completata!")
    print(f"File elaborati: {processed_files}/{total_files}")
    print(f"Tempo totale: {format_time(total_elapsed)}")
    if processed_files > 0:
        print(f"Tempo medio per file: {total_elapsed/processed_files:.1f} secondi")

if __name__ == "__main__":
    # Verifica che Python 3.10 sia utilizzato
    ensure_python_3_10()
    
    # Aggiorna pip e installa correttamente whisper e tqdm
    upgrade_pip_and_install_packages()
    
    while True:
        podcast_dir = input("\nInserisci il percorso della cartella contenente i podcast: ").strip()
        
        if os.path.isdir(podcast_dir):
            print(f"\nIniziando l'elaborazione della cartella: {podcast_dir}")
            main(podcast_dir)
        else:
            print("Il percorso inserito non è valido. Per favore riprova.")
            continue
        
        while True:
            scelta = input("\nUtilizza di nuovo lo script digitando 1 o premi 0 per uscire: ").strip()
            if scelta == '1':
                break
            elif scelta == '0':
                print("Arrivederci!")
                sys.exit(0)
            else:
                print("Scelta non valida. Inserire 1 o 0.")
        
        if scelta == '0':
            break