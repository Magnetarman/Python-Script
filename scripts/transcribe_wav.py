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

def get_supported_audio_formats():
    """
    Restituisce la lista dei formati audio supportati per la conversione.
    Returns:
        list: Lista delle estensioni supportate (senza punto)
    """
    return [
        'wav', 'mp3', 'flac', 'ogg', 'm4a', 'aac',
        'wma', 'opus', 'aiff', 'webm', 'mp4'
    ]

def is_audio_format_supported(file_path):
    """
    Verifica se il formato del file audio è supportato.
    Args:
        file_path: Percorso del file da verificare
    Returns:
        bool: True se il formato è supportato, False altrimenti
    """
    supported_formats = get_supported_audio_formats()
    file_ext = os.path.splitext(file_path)[1][1:].lower()  # Rimuovi il punto e metti minuscolo
    return file_ext in supported_formats

def convert_audio_to_wav(input_path, output_path):
    """
    Converte un file audio in formato WAV utilizzando FFmpeg.
    Args:
        input_path: Percorso del file audio da convertire
        output_path: Percorso del file WAV di destinazione
    Returns:
        bool: True se la conversione è riuscita, False altrimenti
    """
    try:
        # Comando FFmpeg per convertire in WAV mantenendo la qualità originale
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',  # Codec WAV standard
            '-ar', '44100',          # Sample rate 44.1kHz
            '-ac', '2',              # Canali stereo
            output_path
        ]

        print(f"  Conversione in corso: {os.path.basename(input_path)} → WAV")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            print(f"  Conversione completata: {os.path.basename(output_path)}")
            return True
        else:
            print(f"  Errore nella conversione: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("  Timeout nella conversione audio")
        return False
    except FileNotFoundError:
        print("  FFmpeg non trovato. Installa FFmpeg per la conversione audio")
        return False
    except Exception as e:
        print(f"  Errore durante la conversione: {e}")
        return False

def split_audio_into_chunks(input_path, chunk_duration=300):
    """
    Divide un file audio in chunk consecutivi per il processamento parallelo.
    Args:
        input_path: Percorso del file audio da dividere
        chunk_duration: Durata di ogni chunk in secondi (default: 5 minuti)
    Returns:
        list: Lista dei percorsi dei chunk creati, o None se fallisce
    """
    try:
        # Crea directory temporanea per i chunk
        temp_dir = os.path.dirname(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        # Crea i percorsi per i due chunk
        chunk1_path = os.path.join(temp_dir, f"{base_name}_chunk1.wav")
        chunk2_path = os.path.join(temp_dir, f"{base_name}_chunk2.wav")

        # Usa FFprobe per ottenere la durata totale
        ffprobe_cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries',
            'format=duration', '-of', 'csv=p=0', input_path
        ]

        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("  Impossibile ottenere durata audio")
            return None

        total_duration = float(result.stdout.strip())

        # Se l'audio è più corto di chunk_duration * 1.5, elabora come singolo chunk
        if total_duration < chunk_duration * 1.5:
            print(f"  Audio corto ({total_duration:.1f}s), elaborazione singola")
            return [input_path]

        # Calcola punto di divisione (metà circa)
        split_point = total_duration / 2

        print(f"  Divisione audio in 2 chunk da ~{split_point:.1f}s cadauno")

        # Crea primo chunk (da 0 a split_point)
        cmd1 = [
            'ffmpeg', '-y', '-i', input_path,
            '-t', str(split_point),
            '-acodec', 'pcm_s16le', '-ar', '44100',
            chunk1_path
        ]

        # Crea secondo chunk (da split_point a fine)
        cmd2 = [
            'ffmpeg', '-y', '-i', input_path,
            '-ss', str(split_point),
            '-acodec', 'pcm_s16le', '-ar', '44100',
            chunk2_path
        ]

        # Crea i chunk in sequenza
        print("  Creazione chunk 1...")
        result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=60)

        if result1.returncode != 0:
            print("  Errore creazione chunk 1")
            return None

        print("  Creazione chunk 2...")
        result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=60)

        if result2.returncode != 0:
            print("  Errore creazione chunk 2")
            # Pulisce chunk 1 se chunk 2 fallisce
            if os.path.exists(chunk1_path):
                os.remove(chunk1_path)
            return None

        print("  Chunk creati con successo")
        return [chunk1_path, chunk2_path]

    except Exception as e:
        print(f"  Errore durante la divisione audio: {e}")
        return None

def transcribe_chunk_parallel(chunk_path, model_name='medium', language='it'):
    """
    Trascrive un singolo chunk audio utilizzando Whisper.
    Args:
        chunk_path: Percorso del chunk da trascrivere
        model_name: Nome del modello Whisper
        language: Lingua del contenuto
    Returns:
        str: Testo trascritto del chunk
    """
    try:
        whisper, tqdm = import_required_modules()

        # Suppress FP16 warning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
            model = whisper.load_model(model_name)

        # Trascrive il chunk
        result = model.transcribe(chunk_path, language=language)
        return result['text']

    except Exception as e:
        print(f"  Errore nella trascrizione del chunk {os.path.basename(chunk_path)}: {e}")
        return ""

def transcribe_audio_parallel(file_path, model_name='medium', language='it'):
    """
    Trascrive un file audio dividendo in chunk e processando in parallelo.
    Args:
        file_path: Percorso del file audio da trascrivere
        model_name: Nome del modello Whisper
        language: Lingua del contenuto
    Returns:
        str: Testo trascritto completo
    """
    import concurrent.futures
    import time

    print("Avvio trascrizione parallela...")

    # Dividi l'audio in chunk
    chunks = split_audio_into_chunks(file_path)

    if not chunks or len(chunks) == 1:
        # Se non è stato possibile dividere o audio troppo corto, trascrizione singola
        print("Esecuzione trascrizione singola (audio corto o indivisibile)")
        return transcribe_podcast_with_progress(file_path, model_name, language, speed_up=False)

    print(f"Trascrizione parallela di {len(chunks)} chunk...")

    start_time = time.time()

    try:
        # Avvia trascrizione parallela dei chunk
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Invia i job per i due chunk
            future1 = executor.submit(transcribe_chunk_parallel, chunks[0], model_name, language)
            future2 = executor.submit(transcribe_chunk_parallel, chunks[1], model_name, language)

            # Attende i risultati
            print("Elaborazione chunk in corso...")
            chunk1_text = future1.result(timeout=600)  # 10 minuti timeout
            chunk2_text = future2.result(timeout=600)

        # Unisce i risultati
        full_transcription = chunk1_text.strip() + " " + chunk2_text.strip()

        elapsed = time.time() - start_time
        print(f"Trascrizione parallela completata in {elapsed:.1f} secondi")

        # Pulisce i chunk se sono stati creati
        for chunk in chunks:
            if chunk != file_path and os.path.exists(chunk):
                try:
                    os.remove(chunk)
                    print(f"  Chunk {os.path.basename(chunk)} rimosso")
                except Exception as e:
                    print(f"  Attenzione: impossibile rimuovere {chunk}: {e}")

        return full_transcription

    except concurrent.futures.TimeoutError:
        print("Timeout nella trascrizione parallela, fallback a trascrizione singola")
        return transcribe_podcast_with_progress(file_path, model_name, language, speed_up=False)
    except Exception as e:
        print(f"Errore nella trascrizione parallela: {e}, fallback a trascrizione singola")
        return transcribe_podcast_with_progress(file_path, model_name, language, speed_up=False)

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

def transcribe_podcast_with_progress(file_path, model_name='medium', language='it', parallel=False):
    """
    Trascrive un file audio con barra di progresso e opzionale processamento parallelo.
    Args:
        file_path: Percorso del file audio da trascrivere
        model_name: Nome del modello Whisper da utilizzare
        language: Lingua del contenuto audio
        parallel: Se True, utilizza processamento parallelo per velocizzare
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

    # Utilizza processamento parallelo se richiesto
    if parallel:
        return transcribe_audio_parallel(file_path, model_name, language)

    # Altrimenti, trascrizione singola tradizionale
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

    return result['text']

def save_transcription(transcription, output_path):
    """
    Salva la trascrizione in un file di testo.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

def count_supported_audio_files(podcast_dir):
    """
    Conta il numero totale di file audio supportati da elaborare.
    """
    count = 0
    supported_formats = get_supported_audio_formats()

    for root, dirs, files in os.walk(podcast_dir):
        for file_name in files:
            file_ext = os.path.splitext(file_name)[1][1:].lower()
            if file_ext in supported_formats:
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

def main(podcast_dir, parallel=False):
    """
    Funzione principale con barra di progresso e ETA.
    Args:
        podcast_dir: Directory contenente i file audio
        parallel: Se True, utilizza processamento parallelo per velocizzare
    """
    # Importa i moduli necessari
    whisper, tqdm = import_required_modules()
    
    # Conta i file da elaborare
    total_files = count_supported_audio_files(podcast_dir)
    
    if total_files == 0:
        print("Nessun file audio supportato da elaborare trovato.")
        print("Formati supportati: WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4")
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

                # Verifica se il formato è supportato
                if not is_audio_format_supported(file_path):
                    continue

                output_file_name = base_name + '.txt'
                output_path = os.path.join(root, output_file_name)

                # Verifica se la trascrizione esiste già
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1:
                    continue

                # File WAV da utilizzare per la trascrizione (originale o convertito)
                wav_file_path = None
                converted_file_path = None

                try:
                    file_start_time = time.time()

                    # Aggiorna la descrizione con il file corrente
                    main_pbar.set_description(f"Elaborando: {file_name[:30]}...")

                    # Se non è WAV, convertilo
                    if ext.lower() != '.wav':
                        print(f"  Conversione da {ext.upper()[1:]} a WAV richiesta...")
                        converted_file_path = os.path.join(root, base_name + '_converted.wav')
                        if convert_audio_to_wav(file_path, converted_file_path):
                            wav_file_path = converted_file_path
                            print(f"  Conversione completata: {file_name}")
                        else:
                            print(f"  Impossibile convertire {file_name}, salto...")
                            main_pbar.update(1)
                            continue
                    else:
                        # È già WAV, usa il file originale
                        wav_file_path = file_path

                    # Procedi con la trascrizione
                    transcription = transcribe_podcast_with_progress(wav_file_path, parallel=parallel)
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
                finally:
                    # Pulisce il file WAV convertito se è stato creato
                    if converted_file_path and os.path.exists(converted_file_path):
                        try:
                            os.remove(converted_file_path)
                            print("  File WAV convertito rimosso")
                        except Exception as e:
                            print(f"  Attenzione: impossibile rimuovere il file convertito: {e}")
    
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

            # Chiedi se utilizzare il processamento parallelo
            while True:
                parallel_choice = input("Vuoi utilizzare il processamento parallelo per velocizzare la trascrizione? (s/n): ").strip().lower()
                if parallel_choice in ['s', 'si', 'yes', 'y']:
                    parallel = True
                    print("Modalità processamento parallelo attivata")
                    break
                elif parallel_choice in ['n', 'no', 'nope']:
                    parallel = False
                    print("Modalità normale attivata")
                    break
                else:
                    print("Rispondi 's' per sì o 'n' per no.")

            main(podcast_dir, parallel=parallel)
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