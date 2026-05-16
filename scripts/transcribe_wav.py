# Trascrive automaticamente i file audio .wav in testo utilizzando il modello Whisper, 
# salvando le trascrizioni e saltando quelle già esistenti.
import os
import subprocess
import sys
import importlib
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn, MofNCompleteColumn
    console = Console()
except ImportError:
    console = None
import time
import warnings
import threading
import math
from datetime import datetime, timedelta
import argparse
import logging

# Configurazione Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

whisper_lock = threading.Lock()

class ModelCorruptionError(Exception):
    """Eccezione personalizzata per indicare un modello Whisper danneggiato."""
    pass

def safe_print(message):
    """Stampa un messaggio in modo sicuro, interferendo il meno possibile con la barra di progresso."""
    if console:
        console.print(message)
    else:
        print(message)

def setup_file_logging(podcast_dir):
    """
    Configura il logging su file nella directory dei podcast.
    """
    try:
        log_file = os.path.join(podcast_dir, "transcription_debug.log")
        # Rimuovi eventuali handler esistenti per evitare duplicati
        for handler in list(logger.handlers):
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        
        logger.info("-" * 50)
        logger.info(f"AVVIO SESSIONE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Directory: {podcast_dir}")
        logger.info("-" * 50)
        return True
    except Exception as e:
        safe_print(f"⚠️ Impossibile configurare il logging su file: {e}")
        return False

# Lista di stringhe da rimuovere dalla trascrizione
WRONG_SUBSTRINGS = [
  "Sottotitoli e revisione a cura di QTSS.",
  "Sottotitoli e revisione a cura di QTSS",
  "www.mooji.org",
  "Ondertitels ingediend door de Amara.org gemeenschap",
  "Ondertiteld door de Amara.org gemeenschap",
  "Ondertiteling door de Amara.org gemeenschap",
  "Untertitelung aufgrund der Amara.org-Community",
  "Untertitel im Auftrag des ZDF für funk, 2017",
  "Untertitel von Stephanie Geiges",
  "Untertitel der Amara.org-Community",
  "Untertitel im Auftrag des ZDF, 2017",
  "Untertitel im Auftrag des ZDF, 2020",
  "Untertitel im Auftrag des ZDF, 2018",
  "Untertitel im Auftrag des ZDF, 2021",
  "Untertitelung im Auftrag des ZDF, 2021",
  "Copyright WDR 2021",
  "Copyright WDR 2020",
  "Copyright WDR 2019",
  "SWR 2021",
  "SWR 2020",
  "Sous-titres réalisés para la communauté d'Amara.org",
  "Sous-titres réalisés par la communauté d'Amara.org",
  "Sous-titres fait par Sous-titres par Amara.org",
  "Sous-titres réalisés par les SousTitres d'Amara.org",
  "Sous-titres par Amara.org",
  "Sous-titres par la communauté d'Amara.org",
  "Sous-titres réalisés pour la communauté d'Amara.org",
  "Sous-titres réalisés par la communauté de l'Amara.org",
  "Sous-Titres faits par la communauté d'Amara.org",
  "Sous-titres par l'Amara.org",
  "Sous-titres fait par la communauté d'Amara.org",
  "Sous-titrage ST' 501",
  "Sous-titrage ST'501",
  "Merci d'avoir regardé cette vidéo.",
  "Merci d'avoir regardé cette vidéo!",
  "Merci d'avoir regardé cette vidéo !",
  "Merci d'avoir regardé la vidéo.",
  "J'espère que vous avez apprécié la vidéo.",
  "Je vous remercie de vous abonner",
  "Cliquez-vous sur les sous-titres et abonnez-vous à la chaîne d'Amara.org",
  "❤️ par SousTitreur.com",
  "Sottotitoli creati dalla comunità Amara.org",
  "Sottotitoli di Sottotitoli di Amara.org",
  "Sottotitoli e revisione al canale di Amara.org",
  "Sottotitoli e revisione a cura di Amara.org",
  "Sottotitoli e revisione a cura di QTSS.",
  "Sottotitoli e revisione a cura di QTSS",
  "Sottotitoli a cura di QTSS",
  "Sottotitoli creati dalla comunità Amara.org per te.",
  "Subtítulos realizados por la comunidad de Amara.org",
  "Subtitulado por la comunidad de Amara.org",
  "Subtítulos por la comunidad de Amara.org",
  "Subtítulos creados por la comunidad de Amara.org",
  "Subtítulos en español de Amara.org",
  "Subtítulos hechos por la comunidad de Amara.org",
  "Subtitulos por la comunidad de Amara.org",
  "— Sous-titrage ST'501 —",
  "Más información www.alimmenta.com",
  "www.mooji.org",
  "Subtítulos realizados por la comunidad de Amara.org",
  "Legendas pela comunidade Amara.org",
  "Legendas pela comunidade de Amara.org",
  "Legendas pela comunidade do Amara.org",
  "Legendas pela comunidade das Amara.org",
  "Transcrição e Legendas pela comunidade de Amara.org",
  "Sottotitoli creati dalla comunità Amara.org",
  "Sous-titres réalisés para la communauté d'Amara.org",
  "Sous-titres réalisés para la communauté d'Amara.org",
  "Napisy stworzone przez społeczność Amara.org",
  "Napisy wykonane przez społeczność Amara.org",
  "Zdjęcia i napisy stworzone przez społeczność Amara.org",
  "napisy stworzone przez społeczność Amara.org",
  "Tłumaczenie i napisy stworzone przez społeczność Amara.org",
  "Napisy stworzone przez społeczności Amara.org",
  "Tłumaczenie stworzone przez społeczność Amara.org",
  "Napisy robione przez społeczność Amara.org",
  "www.multi-moto.eu",
  "Редактор субтитров А.Синецкая Корректор А.Егорова",
  "Yorumlarınızıza abone olmayı unutmayın.",
  "Sottotitoli creati dalla comunità Amara.org","字幕由Amara.org社区提供",
  "小編字幕由Amara.org社區提供",
  "[Music]",
  "[promo]",
  "[Promo]",
  "♪",
  "(upbeat music)",
  "(Instrumental)",
  "[BLANK_AUDIO]",
  "[ cease fire ]",
  "gu.se",
  "(majestic music)",
  "[Pause]",
  "(snow crunching)",
  "[Sounds of wind blowing]",
  "(gulp)",
  "Sottotitoli e Tsub atki",
  "[silenzio]",
  "[LAUGH]",
  "[ Background noise ]",
  "[Clapping]",
  "[SOUND]",
  "[Sound of metal being hammered against the floor] ",
  "Subtitles by the Amara.org community",
  "Transcripts by the Amara.org community",
  "*laughing*",
  "(laughs)",
  "[laughs]",
  "[Laughter]",
  "*laughter*",
  "(thud)",
  "*laughs*",
  "*lacht*",
  "[BLANK_AUDIO]",
  "[Chuckle]",
  "*Chuckle*",
  "(laughing)",
  "Subs by www.zeoranger.co.uk",
  "*thud*",
  "*sniff*",
  "[BLANK_AU",
  "[BLANK",
  "[Lacht]",
  "[Silence]",
  "[]",
  "(smacking)",
  "[Chuckling]",
  "(air whooshing)",
  "(whooshing)",
  "(sighs)",
  "(blows kiss)",
  "[Musica]",
  "[MUSIC PLAYING]",
  "[BREATHING HEAVILY]",
  "[Whispering]",
  "[BEEPING]",
  "(scratching)",
  "(wind blowing)",
  "(swooshing)",
  "(chicken clucking)",
  "(footsteps crunching)",
  "(beeping)",
  "(birds chirping)",
  "(sniffing)",
  "(footsteps)",
  "Transcribed by https://otter.ai",
  "[SPEAKING ENGLISH]",
  "[AUDIO EN BLANCO]",
  "[AUDIO_EN_BLANCO]",
  "*Crofie*",
  "org Subtítulos realizados por la comunidad de Amara.",
  "(Sonido de campanita)",
  "(Música de suspenso)",
  "Translation & subtitling by Quentin Dewaghe Traduction &-titrage par Quentin Dewaghe q.",
  "Transcription by ESO;",
  "translation by —"
]

def clean_transcription(text):
    """
    Rimuove le stringhe indesiderate dalla trascrizione.
    """
    if not text:
        return ""
        
    cleaned_text = text
    for wrong_string in WRONG_SUBSTRINGS:
        if wrong_string in cleaned_text:
            cleaned_text = cleaned_text.replace(wrong_string, "")
            
    # Rimuove spazi doppi creati dalla rimozione
    import re
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def is_venv():
    """Verifica se lo script è in esecuzione in un virtual environment."""
    return sys.prefix != sys.base_prefix or hasattr(sys, 'real_prefix')

def upgrade_pip_and_install_packages():
    """
    Aggiorna pip e installa o reinstalla correttamente whisper, tqdm e rich.
    """
    python_path = sys.executable
    use_user = not is_venv()
    user_flag = ["--user"] if use_user else []

    safe_print(f"Utilizzo Python: {python_path}")
    if use_user:
        safe_print("Rilevato ambiente globale: utilizzo flag --user per i permessi.")
    
    safe_print("Aggiornamento di pip in corso...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"] + user_flag)
    except subprocess.CalledProcessError as e:
        safe_print(f"⚠️ Nota: Impossibile aggiornare pip (potrebbe non essere critico): {e}")

    safe_print("Installazione di openai-whisper, tqdm e rich...")
    try:
        # Disinstalla preventivamente il modulo 'whisper' che crea conflitti
        safe_print("Rimozione eventuali conflitti...")
        subprocess.run([python_path, "-m", "pip", "uninstall", "-y", "whisper"], capture_output=True)
        
        subprocess.check_call([python_path, "-m", "pip", "install", "-U", "openai-whisper", "tqdm", "rich"] + user_flag)
        importlib.invalidate_caches()
    except subprocess.CalledProcessError as e:
        safe_print("\n" + "!" * 60)
        safe_print("❌ ERRORE CRITICO DURANTE L'INSTALLAZIONE")
        safe_print(f"Dettaglio errore: {e}")
        if os.name == 'nt' and "Accesso negato" in str(e):
            safe_print("\nSintomo: ACCESSO NEGATO (WinError 5)")
            safe_print("Soluzione consigliata:")
            safe_print("1. CHIUDI tutti i programmi che usano Python o Whisper.")
            safe_print("2. Apri il terminale (PowerShell o CMD) come AMMINISTRATORE.")
            safe_print(f"3. Esegui manualmente: {python_path} -m pip install -U openai-whisper tqdm rich")
        else:
            safe_print(f"\nProva a installare manualmente: pip install -U openai-whisper tqdm rich")
        safe_print("!" * 60 + "\n")
        sys.exit(1)

def ensure_python_version():
    """
    Verifica se è in uso una versione compatibile di Python (3.8+).
    """
    if sys.version_info[0] != 3 or sys.version_info[1] < 8:
        print(f"Python {sys.version_info.major}.{sys.version_info.minor} non supportato.")
        print("È richiesto Python 3.8 o superiore.")
        print("Per favore aggiorna Python e riprova.")
        sys.exit(1)

    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")


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
        safe_print(f"  DEBUG: Verifica FFmpeg...")
        # Verifica se FFmpeg è disponibile
        ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        if ffmpeg_check.returncode != 0:
            safe_print(f"  ❌ ERRORE: FFmpeg non trovato o non funzionante")
            safe_print(f"  Dettagli: {ffmpeg_check.stderr}")
            return False

        safe_print(f"  DEBUG: FFprobe check...")
        # Verifica se FFprobe è disponibile
        ffprobe_check = subprocess.run(['ffprobe', '-version'], capture_output=True, text=True, timeout=10)
        if ffprobe_check.returncode != 0:
            safe_print(f"  ❌ ERRORE: FFprobe non trovato o non funzionante")
            return False

        # Comando FFmpeg per convertire in WAV mantenendo la qualità originale
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',  # Codec WAV standard
            '-ar', '16000',          # Sample rate 16kHz
            '-ac', '1',              # Canali mono
            output_path
        ]

        safe_print(f"  DEBUG: Input path: {input_path}")
        safe_print(f"  DEBUG: Output path: {output_path}")
        safe_print(f"  DEBUG: File input esiste: {os.path.exists(input_path)}")
        safe_print(f"  Conversione in corso: {os.path.basename(input_path)} → WAV")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            safe_print(f"  DEBUG: Conversione completata, file size: {os.path.getsize(output_path)} bytes")
            safe_print(f"  Conversione completata: {os.path.basename(output_path)}")
            return True
        else:
            safe_print(f"  ❌ ERRORE nella conversione: {result.stderr}")
            safe_print(f"  DEBUG: Return code: {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        safe_print("  Timeout nella conversione audio")
        return False
    except FileNotFoundError:
        safe_print("  FFmpeg non trovato. Installa FFmpeg per la conversione audio")
        return False
    except Exception as e:
        safe_print(f"  Errore durante la conversione: {e}")
        return False

def split_audio_into_chunks(input_path, num_chunks=3):
    """
    Divide un file audio in chunk consecutivi per il processamento parallelo.
    """
    try:
        # Crea directory temporanea
        temp_dir = os.path.join(os.path.dirname(input_path), "_temp")
        os.makedirs(temp_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        # Ottieni durata totale
        ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', input_path]
        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0: return None
        total_duration = float(result.stdout.strip())

        # Se l'audio è troppo corto (meno di 45s), elaborazione singola
        if total_duration < 45: return [input_path]

        actual_chunks = num_chunks
        # Se l'audio è corto per 3 chunk, prova con 2
        if total_duration < 90 and num_chunks > 2: actual_chunks = 2
        
        segment_duration = total_duration / actual_chunks
        safe_print(f"  ⚡ Divisione audio in {actual_chunks} chunk per elaborazione parallela...")
        
        chunks = []
        for i in range(actual_chunks):
            chunk_path = os.path.join(temp_dir, f"{base_name}_chunk{i+1}.wav")
            start_time = i * segment_duration
            
            # Aggiunge un piccolo overlap di 1s tra i chunk per non perdere sillabe
            # tranne che per il primo chunk
            ss_time = max(0, start_time - 1) if i > 0 else 0
            # Durata: se non è l'ultimo chunk, aggiungiamo l'overlap
            t_duration = segment_duration + (1 if i > 0 else 0) if i < actual_chunks - 1 else None
            
            cmd = ['ffmpeg', '-y', '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1']
            if ss_time > 0: cmd.extend(['-ss', str(ss_time)])
            if t_duration: cmd.extend(['-t', str(t_duration)])
            cmd.append(chunk_path)
            
            subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            chunks.append(chunk_path)
            
        return chunks
    except Exception as e:
        safe_print(f"  ❌ Errore split: {e}")
        return None

def transcribe_chunk_parallel(chunk_path, model, language='it'):
    """
    Trascrive un singolo chunk audio utilizzando Whisper.
    """
    try:
        safe_print(f"  DEBUG: Inizio trascrizione chunk {os.path.basename(chunk_path)}")

        # Verifica che il chunk esista e sia valido
        if not os.path.exists(chunk_path):
            safe_print(f"  ❌ ERRORE: Chunk non trovato: {chunk_path}")
            return ""

        chunk_size = os.path.getsize(chunk_path)
        safe_print(f"  DEBUG: Chunk size: {chunk_size} bytes")

        if chunk_size < 1000:
            safe_print(f"  ❌ ERRORE: Chunk troppo piccolo: {chunk_size} bytes")
            return ""

        # Verifica che il modello sia valido
        if not hasattr(model, 'transcribe'):
            safe_print(f"  ❌ ERRORE: Modello non valido, manca metodo transcribe")
            return ""

        # Trascrive il chunk usando il modello già caricato
        logger.debug(f"Avvio model.transcribe per {os.path.basename(chunk_path)}")
        safe_print(f"  DEBUG: Avvio trascrizione con modello {type(model)}")
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
                with whisper_lock:
                    result = model.transcribe(chunk_path, language=language)
            logger.debug(f"Trascrizione completata per {os.path.basename(chunk_path)}")
            safe_print(f"  DEBUG: Trascrizione completata per {os.path.basename(chunk_path)}")
            return clean_transcription(result['text'])
        except (AttributeError, KeyError) as e:
            err_msg = str(e)
            is_model_error = any(x in err_msg for x in ["Linear", "KeyError", "decoder", "encoder"])
            is_corruption_symptom = any(x in err_msg for x in ["NoneType", "attribute", "forward", "object has no"])
            
            if is_model_error and (is_corruption_symptom or "KeyError" in type(e).__name__ or "Linear" in err_msg):
                raise ModelCorruptionError(err_msg)
            else:
                raise e
        except RuntimeError as e:
            if "cannot reshape tensor of 0 elements" in str(e):
                safe_print(f"  ⚠️ ATTENZIONE: Chunk {os.path.basename(chunk_path)} sembra vuoto o silenzioso (RuntimeError tensor 0). Salto.")
                return ""
            raise e

    except ModelCorruptionError as e:
        raise e
    except Exception as e:
        logger.exception(f"❌ ERRORE nella trascrizione del chunk {os.path.basename(chunk_path)}")
        safe_print(f"  ❌ ERRORE nella trascrizione del chunk {os.path.basename(chunk_path)}: {e}")
        return ""

def transcribe_audio_parallel(file_path, model, language='it'):
    """
    Trascrive un file audio dividendo in chunk e processando in parallelo.
    """
    import concurrent.futures
    import time
    import threading

    logger.info(f"Inizio trascrizione parallela per: {file_path}")
    safe_print("Avvio trascrizione parallela...")

    # Ottieni la durata per la barra di progresso
    audio_duration = get_audio_duration(file_path)

    # Dividi l'audio in chunk (3 segmenti per default)
    chunks = split_audio_into_chunks(file_path, num_chunks=3)

    if not chunks or len(chunks) <= 1:
        safe_print("Esecuzione trascrizione singola (audio troppo corto o indivisibile)")
        return transcribe_podcast_with_progress(file_path, model, language, parallel=False)

    actual_chunks = len(chunks)
    logger.info(f"Audio diviso in {actual_chunks} chunk")
    safe_print(f"⚡ Elaborazione di {actual_chunks} chunk in parallelo...")

    start_time = time.time()
    progress_thread = None
    transcription_done = False
    progress = None
    task_id = None

    try:
        if console:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=None),
                TaskProgressColumn(),
                TextColumn("•"),
                TimeRemainingColumn(),
                TextColumn("•"),
                TextColumn("[cyan]{task.fields[info]}"),
                console=console
            )
            progress.start()
            task_id = progress.add_task("🚀 Elaborazione Parallela", total=100, info="")

        def update_progress():
            nonlocal transcription_done, progress, task_id, start_time, audio_duration, actual_chunks
            while not transcription_done:
                if progress is None or task_id is None:
                    time.sleep(0.5)
                    continue
                
                elapsed = time.time() - start_time
                if elapsed > 0:
                    estimated_total_time = (audio_duration * 0.15) / (actual_chunks * 0.75)
                    estimated_progress = min(99.0, (elapsed / estimated_total_time) * 100) if estimated_total_time > 0 else 0
                else:
                    estimated_progress = 0

                speed = estimated_progress / elapsed if elapsed > 0 else 0
                progress.update(task_id, completed=estimated_progress, info=f"Audio: {audio_duration:.0f}s | Speed: {speed:.1f}%/s")
                time.sleep(0.5)

        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers=actual_chunks, thread_name_prefix="WhisperWorker") as executor:
            logger.debug(f"Invio job a ThreadPoolExecutor con {actual_chunks} worker")
            futures = [executor.submit(transcribe_chunk_parallel, chunk, model, language) for chunk in chunks]

            try:
                chunk_timeout = int(max(1500, audio_duration // actual_chunks + 600))
                results_text = [future.result(timeout=chunk_timeout) for future in futures]

            except concurrent.futures.TimeoutError:
                logger.error(f"Timeout nella trascrizione parallela per {file_path}")
                safe_print("Timeout nella trascrizione parallela, fallback a trascrizione singola")
                transcription_done = True
                if progress: progress.stop()
                return transcribe_podcast_with_progress(file_path, model, language, parallel=False)
            except ModelCorruptionError as e:
                transcription_done = True
                if progress: progress.stop()
                raise e
            except Exception as e:
                transcription_done = True
                if progress: progress.stop()
                raise e

            full_transcription = " ".join([t.strip() for t in results_text if t])
            elapsed = time.time() - start_time
            safe_print(f"✅ Trascrizione parallela ({actual_chunks} chunk) completata in {elapsed:.1f} secondi")

        return full_transcription

    finally:
        transcription_done = True
        if progress_thread is not None:
            try: progress_thread.join(timeout=1.0)
            except: pass
                
        if progress and task_id is not None:
            try: progress.update(task_id, completed=100, info="Completato!")
            except: pass
            try: progress.stop()
            except: pass

        try:
            for chunk in chunks:
                if chunk != file_path and os.path.exists(chunk):
                    try: os.remove(chunk)
                    except: pass
            
            temp_dir = os.path.join(os.path.dirname(file_path), "_temp")
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)
        except: pass


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

def transcribe_podcast_with_progress(file_path, model, language='it', parallel=False):
    """
    Trascrive un file audio con barra di progresso e opzionale processamento parallelo.
    Args:
        file_path: Percorso del file audio da trascrivere
        model: Modello Whisper già caricato
        language: Lingua del contenuto audio
        parallel: Se True, utilizza processamento parallelo per velocizzare
    """
    safe_print(f"  DEBUG: transcribe_podcast_with_progress chiamato per {os.path.basename(file_path)}")

    # Ottieni la durata effettiva del file audio
    safe_print("Analisi del file audio...")
    audio_duration = get_audio_duration(file_path)
    safe_print(f"Durata audio rilevata: {audio_duration:.1f} secondi")

    # Calcola i chunk da 30 secondi
    chunk_duration = 30.0  # secondi
    total_chunks = math.ceil(audio_duration / chunk_duration)
    safe_print(f"Divisione in {total_chunks} chunk da {chunk_duration} secondi cadauno")

    safe_print("Trascrizione in corso...")

    # Utilizza processamento parallelo se richiesto
    if parallel:
        return transcribe_audio_parallel(file_path, model, language)

    # Altrimenti, trascrizione singola tradizionale
    start_time = time.time()
    transcription_done = False
    progress_thread = None

    # Barra di progresso per la trascrizione singola usando rich
    progress = None
    task_id = None
    if console:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            BarColumn(bar_width=None),
            TaskProgressColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            TextColumn("•"),
            TextColumn("[yellow]{task.fields[info]}"),
            console=console
        )
        progress.start()
        task_id = progress.add_task("🎵 Trascrizione Audio", total=100, info="")
    
    # Avvia la trascrizione con soppressione del warning FP16
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

        def update_progress():
            """Aggiorna la barra di progresso basata su stime temporali"""
            nonlocal transcription_done, progress, task_id, start_time, audio_duration

            if progress is None or task_id is None:
                return

            processing_ratio = 0.15  # secondi di processing per secondo di audio

            while not transcription_done:
                elapsed = time.time() - start_time
                estimated_progress = min(99.0, (elapsed / (audio_duration * processing_ratio)) * 100)

                # Calcola velocità
                speed = estimated_progress / elapsed if elapsed > 0 else 0
                
                # Aggiorna la barra
                progress.update(task_id, completed=estimated_progress, info=f"Audio: {audio_duration:.0f}s | Speed: {speed:.1f}%/s")

                time.sleep(0.5)

        # Avvia il thread per l'aggiornamento del progresso
        if progress:
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()

        # Verifica che il file esista prima della trascrizione
        if not os.path.exists(file_path):
            safe_print(f"  ❌ ERRORE: File non trovato per trascrizione: {file_path}")
            return ""

        # Esegue la trascrizione
        safe_print(f"  DEBUG: Esecuzione trascrizione per {os.path.basename(file_path)}")
        try:
            result = model.transcribe(file_path, language=language)
            safe_print(f"  DEBUG: Trascrizione completata con successo")
        except (AttributeError, KeyError) as e:
            err_msg = str(e)
            is_model_error = any(x in err_msg for x in ["Linear", "KeyError", "decoder", "encoder"])
            is_corruption_symptom = any(x in err_msg for x in ["NoneType", "attribute", "forward", "object has no"])
            
            if is_model_error and (is_corruption_symptom or "KeyError" in type(e).__name__ or "Linear" in err_msg):
                raise ModelCorruptionError(err_msg)
            else:
                raise e

    # Completa la barra di progresso
    transcription_done = True
    if progress_thread is not None:
        progress_thread.join(timeout=1.0)
        
    elapsed = time.time() - start_time
    if progress and task_id is not None:
        progress.update(task_id, completed=100, info=f"Fine: {elapsed:.1f}s")
        progress.stop()

    return clean_transcription(result['text'])

def save_transcription(transcription, output_path):
    """
    Salva la trascrizione in un file di testo.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

def count_supported_audio_files(podcast_dir):
    """
    Conta il numero totale di file audio supportati da elaborare.
    Esclude la directory _temp per evitare di contare i chunk temporanei.
    Conta i file che hanno .txt vuoto o inesistente (consistente con la logica di main).
    """
    count = 0
    supported_formats = get_supported_audio_formats()

    for root, dirs, files in os.walk(podcast_dir):
        # Salta la directory _temp per evitare di contare i chunk temporanei
        dirs[:] = [d for d in dirs if d != '_temp']

        for file_name in files:
            if file_name.endswith('_converted.wav'):
                continue
            file_ext = os.path.splitext(file_name)[1][1:].lower()
            if file_ext in supported_formats:
                base_name = os.path.splitext(file_name)[0]
                output_path = os.path.join(root, base_name + '.txt')
                # Conta solo se il file .txt NON esiste o è vuoto (≤10 bytes)
                if not os.path.exists(output_path) or os.path.getsize(output_path) <= 10:
                    count += 1
                    print(f"  📝 File da elaborare: {file_name}")
                else:
                    print(f"  ⏭️ File già trascritto: {file_name} ({os.path.getsize(output_path)} bytes)")
    return count

def format_time(seconds):
    """
    Formatta i secondi in formato HH:MM:SS.
    """
    return str(timedelta(seconds=int(seconds)))

def main(podcast_dir, model_name='medium', language='it', parallel=False, force_reprocess=False):
    """
    Funzione principale con barra di progresso, ETA e gestione recupero errori.
    """
    setup_file_logging(podcast_dir)
    logger.info(f"Inizio main loop - Model: {model_name}, Lang: {language}, Parallel: {parallel}")
    
    retry_count = 0
    max_retries = 1
    current_force_reprocess = force_reprocess

    while retry_count <= max_retries:
        try:
            # Importa i moduli necessari
            try:
                # Forza la precedenza dei pacchetti installati dall'utente per evitare conflitti con pacchetti di sistema
                import site
                user_site = site.getusersitepackages()
                if user_site and user_site not in sys.path:
                    sys.path.insert(0, user_site)
                
                import whisper
                
                # Verifica se è il modulo whisper corretto (OpenAI) o quello sbagliato (Graphite)
                if not hasattr(whisper, 'load_model'):
                    safe_print("⚠️ Rilevato modulo 'whisper' errato (conflitto installazione).")
                    raise ImportError("Wrong whisper module")
                    
                from rich.progress import Progress
                safe_print(f"Moduli importati correttamente: whisper {whisper.__version__ if hasattr(whisper, '__version__') else 'OK'}, rich OK")
            except ImportError as e:
                safe_print(f"Moduli non trovati: {e}. Installazione in corso...")
                upgrade_pip_and_install_packages()

                try:
                    import whisper
                    from rich.progress import Progress
                    safe_print(f"Moduli installati e importati correttamente: whisper {whisper.__version__ if hasattr(whisper, '__version__') else 'OK'}, rich OK")
                except ImportError as e:
                    safe_print(f"Impossibile importare i moduli anche dopo l'installazione: {e}")
                    safe_print("Prova a installare manualmente i moduli: pip install openai-whisper tqdm rich")
                    sys.exit(1)

            # Carica il modello Whisper con fallback automatico
            safe_print(f"Caricamento del modello {model_name}...")

            # Lista di modelli da provare in ordine di preferenza
            model_names = [model_name, 'base', 'small', 'tiny']

            model = None
            for attempt_model in model_names:
                try:
                    safe_print(f"  DEBUG: Tentativo con modello {attempt_model}")
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
                        model = whisper.load_model(attempt_model)

                    # Verifica che il modello sia valido
                    if hasattr(model, 'transcribe'):
                        safe_print(f"✅ SUCCESSO: Modello {attempt_model} caricato correttamente")
                        if attempt_model != model_name:
                            safe_print(f"⚠️  ATTENZIONE: Usato modello {attempt_model} invece di {model_name}")
                        break
                    else:
                        safe_print(f"❌ ERRORE: Modello {attempt_model} caricato ma non valido")
                        model = None

                except Exception as e:
                    safe_print(f"❌ ERRORE: Impossibile caricare il modello {attempt_model}: {e}")
                    model = None
                    continue

            if model is None:
                safe_print(f"❌ ERRORE CRITICO: Impossibile caricare alcun modello Whisper valido")
                safe_print("Verifica l'installazione di Whisper e PyTorch")
                safe_print("Se il problema persiste, prova a reinstallare:")
                safe_print("  pip uninstall openai-whisper torch torchvision torchaudio")
                safe_print("  pip install openai-whisper")
                return

            safe_print(f"DEBUG: Modello verificato, pronto per la trascrizione")

            # Conta i file da elaborare
            total_files = count_supported_audio_files(podcast_dir)
            
            if total_files == 0:
                safe_print("Nessun file audio supportato da elaborare trovato.")
                safe_print("Formati supportati: WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4")
                return
            
            safe_print(f"\nTrovati {total_files} file da trascrivere.")
            
            processed_files = 0
            start_time = time.time()
            processed_file_list = []  # Lista per tracciare file già elaborati
            
            # Barra di progresso principale per tutti i file usando rich
            main_progress = None
            main_task_id = None
            if console:
                main_progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[bold magenta]📁 Elaborazione File[/bold magenta]"),
                    BarColumn(style="magenta"),
                    MofNCompleteColumn(),
                    TextColumn("•"),
                    TimeElapsedColumn(),
                    TextColumn("•"),
                    TextColumn("[italic cyan]{task.fields[status]}"),
                    console=console
                )
                main_progress.start()
                main_task_id = main_progress.add_task("Main", total=total_files, status="Avvio...")
            
            for root, dirs, files in os.walk(podcast_dir):
                # Salta la directory _temp per evitare di processare i chunk temporanei
                dirs[:] = [d for d in dirs if d != '_temp']

                for file_name in files:
                    if file_name.endswith('_converted.wav'):
                        continue
                    file_path = os.path.join(root, file_name)
                    base_name, ext = os.path.splitext(file_name)

                    # Verifica se il formato è supportato
                    if not is_audio_format_supported(file_path):
                        continue

                    output_file_name = base_name + '.txt'
                    output_path = os.path.join(root, output_file_name)

                    # Verifica se la trascrizione esiste già e contiene dati significativi
                    if os.path.exists(output_path) and not current_force_reprocess:
                        txt_size = os.path.getsize(output_path)
                        safe_print(f"  DEBUG: File .txt esistente: {output_path} ({txt_size} bytes)")
                        if txt_size > 10:  # Più di 10 byte = probabilmente contiene trascrizione
                            safe_print(f"  ⏭️  Trascrizione già esistente per: {file_name} ({txt_size} bytes)")
                            if main_progress and main_task_id is not None:
                                main_progress.update(main_task_id, advance=1, status=f"Saltato: {file_name[:20]}")
                            continue
                        else:
                            safe_print(f"  ⚠️  File .txt esistente ma vuoto o quasi ({txt_size} bytes) - rielaboro")
                    else:
                        safe_print(f"  DEBUG: Nessun file .txt esistente per {file_name}")

                    # Verifica se il file è già stato elaborato in questa sessione
                    if file_path in processed_file_list:
                        safe_print(f"  ⏭️  File già elaborato in questa sessione: {file_name}")
                        if main_progress and main_task_id is not None:
                            main_progress.update(main_task_id, advance=1, status=f"Già fatto: {file_name[:20]}")
                        continue

                    safe_print(f"  📝  Elaborazione file: {file_name}")
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        if file_size < 1000:  # Meno di 1KB è probabilmente non valido
                            safe_print(f"  ❌ ERRORE: File troppo piccolo ({file_size} bytes), probabilmente non è un file audio valido")
                            if main_progress and main_task_id is not None:
                                main_progress.update(main_task_id, advance=1, status=f"ERRORE: {file_name[:20]}")
                            continue
                    else:
                        safe_print(f"  ❌ ERRORE: File non esiste: {file_path}")
                        if main_progress and main_task_id is not None:
                            main_progress.update(main_task_id, advance=1, status=f"Non trovato: {file_name[:20]}")
                        continue

                    # File WAV da utilizzare per la trascrizione (originale o convertito)
                    wav_file_path = None
                    converted_file_path = None

                    try:
                        file_start_time = time.time()

                        # Aggiorna la descrizione con il file corrente
                        if main_progress and main_task_id is not None:
                            main_progress.update(main_task_id, status=f"Lavorando: {file_name[:30]}...")

                        # Se non è WAV, convertilo
                        if ext.lower() != '.wav':
                            converted_file_path = os.path.join(root, base_name + '_converted.wav')
                            if convert_audio_to_wav(file_path, converted_file_path):
                                wav_file_path = converted_file_path
                                safe_print(f"  Conversione completata: {file_name}")
                            else:
                                safe_print(f"  ❌ Impossibile convertire {file_name}, salto...")
                                if main_progress and main_task_id is not None:
                                    main_progress.update(main_task_id, advance=1, status=f"Fallito: {file_name[:20]}")
                                continue
                        else:
                            wav_file_path = file_path

                        # Procedi con la trascrizione
                        transcription = transcribe_podcast_with_progress(wav_file_path, model, language, parallel)
                        save_transcription(transcription, output_path)

                        # Aggiungi il file alla lista dei processati
                        processed_file_list.append(file_path)
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
                        if main_progress and main_task_id is not None:
                            main_progress.update(main_task_id, advance=1, status=f"Completato: {file_name[:20]}")

                        safe_print(f"\n✅ Completato: {file_name}")
                        safe_print(f"💾 Salvato in: {output_path}")
                        safe_print(f"⏱️  Tempo impiegato: {file_elapsed:.1f} secondi")
                        logger.info(f"File completato: {file_name} in {file_elapsed:.1f}s")

                    except ModelCorruptionError as e:
                        # Rilancia l'eccezione per essere catturata dal loop esterno
                        raise e
                    except Exception as e:
                        safe_print(f"\n❌ Errore durante la trascrizione di {file_name}: {e}")
                        if main_progress and main_task_id is not None:
                            main_progress.update(main_task_id, advance=1, status=f"ERRORE: {file_name[:20]}")
                    finally:
                        # Pulisce il file WAV convertito se è stato creato
                        if converted_file_path and os.path.exists(converted_file_path):
                            try:
                                os.remove(converted_file_path)
                            except Exception as e:
                                safe_print(f"  Attenzione: impossibile rimuovere il file convertito: {e}")
            
            total_elapsed = time.time() - start_time
            # Conta file saltati
            skipped_files = total_files - processed_files

            safe_print(f"\n🎉 Trascrizione completata!")
            safe_print(f"📊 File elaborati: {processed_files}")
            if skipped_files > 0:
                safe_print(f"⏭️  File saltati (già esistenti): {skipped_files}")
            safe_print(f"📁 Totale file trovati: {total_files}")
            safe_print(f"⏱️  Tempo totale: {format_time(total_elapsed)}")
            if processed_files > 0:
                safe_print(f"📈 Tempo medio per file: {total_elapsed/processed_files:.1f} secondi")
            
            logger.info(f"Sessione completata con successo. Processati {processed_files}/{total_files} file.")
            break # Successo, esce dal loop retry

        except ModelCorruptionError as e:
            retry_count += 1
            # Ferma la barra di progresso prima della riparazione per pulizia UI
            if main_progress:
                main_progress.stop()
            
            logger.warning(f"RILEVATO ModelCorruptionError: {e}")
            safe_print(f"\n⚠️ ERRORE MODELLO RILEVATO: {e}")
            if retry_count <= max_retries:
                safe_print("Riavvio della trascrizione da zero (tutti i file)...\n")
                current_force_reprocess = True # Forza rielaborazione totale
                # Ricarica moduli per sicurezza
                import whisper
                importlib.reload(whisper)
                continue
            safe_print("❌ Impossibile recuperare il modello dopo tentativi.")
            return
        except Exception as e:
            logger.exception("ERRORE INASPETTATO NEL MAIN LOOP")
            safe_print(f"❌ Errore inaspettato: {e}")
            raise e



def parse_arguments():
    """
    Analizza gli argomenti da riga di comando.
    """
    parser = argparse.ArgumentParser(description="Trascrizione automatica file audio con Whisper.")
    parser.add_argument("--dir", type=str, help="Directory contenente i file audio")
    parser.add_argument("--model", type=str, default="medium", help="Modello Whisper da utilizzare (tiny, base, small, medium, large)")
    parser.add_argument("--lang", type=str, default="it", help="Lingua dell'audio (es. it, en)")
    parser.add_argument("--parallel", action="store_true", help="Abilita trascrizione parallela")
    parser.add_argument("--no-parallel", action="store_false", dest="parallel", help="Disabilita trascrizione parallela")
    parser.set_defaults(parallel=False)
    
    return parser.parse_args()

if __name__ == "__main__":
    # Verifica che sia utilizzata una versione compatibile di Python
    ensure_python_version()

    # La versione aggiornata di whisper e tqdm viene controllata solo se manca l'import
    args = parse_arguments()
    
    # Se viene passato un argomento directory, esegui in modalità non interattiva
    if args.dir:
        if os.path.isdir(args.dir):
            print(f"\nIniziando l'elaborazione della cartella: {args.dir}")
            print(f"Modello: {args.model}, Lingua: {args.lang}, Parallelo: {args.parallel}")
            main(args.dir, model_name=args.model, language=args.lang, parallel=args.parallel)
        else:
            print(f"❌ Errore: La directory {args.dir} non esiste.")
            sys.exit(1)
    else:
        # Modalità interattiva
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

                main(podcast_dir, model_name='medium', language='it', parallel=parallel)
            else:
                print("Il percorso inserito non è valido. Per favori riprova.")
                continue
            
            while True:
                scelta = input("\n🔄 Utilizzare di nuovo lo script con una nuova cartella? (1=sì, 0=no): ").strip()
                if scelta == '1':
                    break
                elif scelta == '0':
                    print("👋 Arrivederci!")
                    sys.exit(0)
                else:
                    print("❌ Scelta non valida. Inserire 1 o 0.")