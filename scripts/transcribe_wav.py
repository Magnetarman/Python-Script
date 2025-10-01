# Trascrive automaticamente i file audio .wav in testo utilizzando il modello Whisper, 
# salvando le trascrizioni e saltando quelle già esistenti.
import os
import subprocess
import sys
import importlib
import time
import warnings
import threading
import math
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

        # Ensure we're running from the correct directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.check_call([python_path, os.path.abspath(__file__)] + sys.argv[1:], cwd=script_dir)
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

def speed_up_audio(input_path, output_path, speed_factor=2.0):
    """
    Accelera un file audio utilizzando FFmpeg.
    Args:
        input_path: Percorso del file audio originale
        output_path: Percorso del file audio accelerato
        speed_factor: Fattore di velocità (2.0 = 2x velocità)
    Returns:
        bool: True se l'operazione è riuscita, False altrimenti
    """
    try:
        # Comando FFmpeg per accelerare l'audio mantenendo il pitch
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-filter:a', f'atempo={speed_factor}',
            '-vn', output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print(f"  Audio accelerato {speed_factor}x: {os.path.basename(input_path)}")
            return True
        else:
            print(f"  Errore nell'accelerazione audio: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("  Timeout nell'accelerazione audio")
        return False
    except FileNotFoundError:
        print("  FFmpeg non trovato. Installa FFmpeg per utilizzare la velocità 2x")
        return False
    except Exception as e:
        print(f"  Errore durante l'accelerazione: {e}")
        return False

def get_audio_duration(file_path):
    """
    Determina la durata effettiva del file audio in secondi.
    Prova diversi metodi per ottenere la durata precisa.
    """
    try:
        # Metodo 1: Usa pydub se disponibile
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(file_path)
            return len(audio) / 1000.0  # pydub restituisce in millisecondi
        except ImportError:
            pass

        # Metodo 2: Usa librosa se disponibile
        try:
            import librosa
            duration = librosa.get_duration(path=file_path)
            return duration
        except ImportError:
            pass

        # Metodo 3: Usa soundfile se disponibile
        try:
            import soundfile as sf
            info = sf.info(file_path)
            return info.duration
        except ImportError:
            pass

        # Metodo 4: Usa ffmpeg se disponibile (fallback)
        try:
            import subprocess
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-show_entries',
                'format=duration', '-of', 'csv=p=0', file_path
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass

        # Metodo 5: Stima basata sulla dimensione del file (fallback)
        file_size = os.path.getsize(file_path)
        # Stima più accurata: ~0.17MB per minuto di audio WAV a 16-bit 44.1kHz mono
        estimated_duration = file_size / (1024 * 1024) * 360  # 360 secondi per MB
        return max(estimated_duration, 30)  # Minimo 30 secondi

    except Exception:
        return 300  # Default 5 minuti se tutti i metodi falliscono

def transcribe_podcast_with_progress(file_path, model_name='medium', language='it', speed_up=False):
    """
    Trascrive un file audio con barra di progresso basata su chunk temporali.
    Args:
        file_path: Percorso del file audio da trascrivere
        model_name: Nome del modello Whisper da utilizzare
        language: Lingua del contenuto audio
        speed_up: Se True, accelera l'audio 2x prima della trascrizione
    """
    whisper, tqdm = import_required_modules()

    print(f"Caricamento del modello {model_name}...")
    # Suppress FP16 warning
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        model = whisper.load_model(model_name)

    # Ottieni la durata effettiva del file audio
    print("Analisi del file audio...")
    audio_duration = get_audio_duration(file_path)
    print(f"Durata audio rilevata: {audio_duration:.1f} secondi")

    # Calcola i chunk da 30 secondi
    chunk_duration = 30.0  # secondi
    total_chunks = math.ceil(audio_duration / chunk_duration)
    print(f"Divisione in {total_chunks} chunk da {chunk_duration} secondi cadauno")

    print("Trascrizione in corso...")

    # Crea file temporaneo se necessario per velocità 2x
    temp_file_path = None
    actual_file_path = file_path

    if speed_up:
        print("Accelerazione audio 2x in corso...")
        temp_dir = os.path.dirname(file_path)
        temp_filename = f"temp_speedup_{os.path.basename(file_path)}"
        temp_file_path = os.path.join(temp_dir, temp_filename)

        if speed_up_audio(file_path, temp_file_path, 2.0):
            actual_file_path = temp_file_path
            print("  Audio accelerato con successo")
        else:
            print("  Impossibile accelerare l'audio, utilizzo file originale")
            actual_file_path = file_path

    start_time = time.time()

    # Barra di progresso basata su chunk completati
    with tqdm(total=100, desc="Progresso", unit="%", ncols=80) as pbar:
        # Avvia la trascrizione con soppressione del warning FP16
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

            def update_progress():
                """Aggiorna la barra di progresso basata su stime temporali"""
                import time

                # Simula il progresso basato sulla durata stimata
                # Whisper processa circa 1 secondo di audio ogni 0.1-0.2 secondi su CPU
                processing_ratio = 0.15  # secondi di processing per secondo di audio

                while not pbar.disable:
                    elapsed = time.time() - start_time
                    # Calcola il progresso basato sul tempo trascorso vs tempo stimato
                    estimated_progress = min(95, (elapsed / (audio_duration * processing_ratio)) * 100)

                    if estimated_progress >= pbar.n:
                        pbar.update(estimated_progress - pbar.n)
                        pbar.set_postfix({
                            "Elaborazione": f"{estimated_progress:.1f}%",
                            "Durata": f"{audio_duration:.1f}s"
                        })

                    time.sleep(0.5)  # Aggiorna ogni 0.5 secondi

            # Avvia il thread per l'aggiornamento del progresso
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()

            # Esegue la trascrizione
            result = model.transcribe(actual_file_path, language=language)

        # Completa la barra di progresso
        elapsed = time.time() - start_time
        pbar.update(100 - pbar.n)  # Completa fino al 100%
        pbar.set_postfix({
            "Tempo": f"{elapsed:.1f}s",
            "Durata": f"{audio_duration:.1f}s"
        })

    # Pulisce il file temporaneo se è stato creato
    if temp_file_path and os.path.exists(temp_file_path):
        try:
            os.remove(temp_file_path)
            print("  File temporaneo rimosso")
        except Exception as e:
            print(f"  Attenzione: impossibile rimuovere il file temporaneo: {e}")

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

def main(podcast_dir, speed_up=False):
    """
    Funzione principale con barra di progresso e ETA.
    Args:
        podcast_dir: Directory contenente i file audio
        speed_up: Se True, accelera l'audio 2x prima della trascrizione
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
                        
                        transcription = transcribe_podcast_with_progress(file_path, speed_up=speed_up)
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

            # Chiedi se utilizzare la velocità 2x
            while True:
                speed_choice = input("Vuoi accelerare l'audio a 2x velocità per velocizzare la trascrizione? (s/n): ").strip().lower()
                if speed_choice in ['s', 'si', 'yes', 'y']:
                    speed_up = True
                    print("Modalità velocità 2x attivata")
                    break
                elif speed_choice in ['n', 'no', 'nope']:
                    speed_up = False
                    print("Modalità normale attivata")
                    break
                else:
                    print("Rispondi 's' per sì o 'n' per no.")

            main(podcast_dir, speed_up=speed_up)
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