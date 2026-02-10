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
import argparse
import logging

# Configurazione Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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

def upgrade_pip_and_install_packages():
    """
    Aggiorna pip e installa o reinstalla correttamente whisper e tqdm.
    Utilizza il Python corrente invece di forzare Python 3.10.
    """
    python_path = sys.executable

    print(f"Utilizzo Python: {python_path}")
    print("Aggiornamento di pip in corso...")
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'aggiornamento di pip: {e}")
        print("Continuo con l'installazione...")

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
        print("Prova a installare manualmente: pip install openai-whisper tqdm")
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

def import_required_modules():
    """
    Importa i moduli necessari in modo sicuro.
    """
    try:
        import whisper
        from tqdm import tqdm
        print(f"Moduli importati correttamente: whisper {whisper.__version__ if hasattr(whisper, '__version__') else 'OK'}, tqdm OK")
        return whisper, tqdm
    except ImportError as e:
        print(f"Moduli non trovati: {e}. Installazione in corso...")
        upgrade_pip_and_install_packages()

        try:
            import whisper
            from tqdm import tqdm
            print(f"Moduli installati e importati correttamente: whisper {whisper.__version__ if hasattr(whisper, '__version__') else 'OK'}, tqdm OK")
            return whisper, tqdm
        except ImportError as e:
            print(f"Impossibile importare i moduli anche dopo l'installazione: {e}")
            print("Prova a installare manualmente i moduli: pip install openai-whisper tqdm")
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
        print(f"  DEBUG: Verifica FFmpeg...")
        # Verifica se FFmpeg è disponibile
        ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        if ffmpeg_check.returncode != 0:
            print(f"  ❌ ERRORE: FFmpeg non trovato o non funzionante")
            print(f"  Dettagli: {ffmpeg_check.stderr}")
            return False

        print(f"  DEBUG: FFprobe check...")
        # Verifica se FFprobe è disponibile
        ffprobe_check = subprocess.run(['ffprobe', '-version'], capture_output=True, text=True, timeout=10)
        if ffprobe_check.returncode != 0:
            print(f"  ❌ ERRORE: FFprobe non trovato o non funzionante")
            return False

        # Comando FFmpeg per convertire in WAV mantenendo la qualità originale
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',  # Codec WAV standard
            '-ar', '44100',          # Sample rate 44.1kHz
            '-ac', '2',              # Canali stereo
            output_path
        ]

        print(f"  DEBUG: Input path: {input_path}")
        print(f"  DEBUG: Output path: {output_path}")
        print(f"  DEBUG: File input esiste: {os.path.exists(input_path)}")
        print(f"  Conversione in corso: {os.path.basename(input_path)} → WAV")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            print(f"  DEBUG: Conversione completata, file size: {os.path.getsize(output_path)} bytes")
            print(f"  Conversione completata: {os.path.basename(output_path)}")
            return True
        else:
            print(f"  ❌ ERRORE nella conversione: {result.stderr}")
            print(f"  DEBUG: Return code: {result.returncode}")
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
        print(f"  DEBUG: split_audio_into_chunks chiamato per {input_path}")
        print(f"  DEBUG: File esiste: {os.path.exists(input_path)}")
        print(f"  DEBUG: File size: {os.path.getsize(input_path) if os.path.exists(input_path) else 'N/A'}")

        # Crea directory temporanea per i chunk nella sottocartella _temp
        temp_dir = os.path.join(os.path.dirname(input_path), "_temp")
        print(f"  DEBUG: Temp dir: {temp_dir}")
        os.makedirs(temp_dir, exist_ok=True)  # Crea la directory se non esiste
        print(f"  DEBUG: Temp dir creata/verificata")
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        # Crea i percorsi per i due chunk nella sottocartella _temp
        chunk1_path = os.path.join(temp_dir, f"{base_name}_chunk1.wav")
        chunk2_path = os.path.join(temp_dir, f"{base_name}_chunk2.wav")
        print(f"  DEBUG: Chunk1 path: {chunk1_path}")
        print(f"  DEBUG: Chunk2 path: {chunk2_path}")

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

def transcribe_chunk_parallel(chunk_path, model, language='it'):
    """
    Trascrive un singolo chunk audio utilizzando Whisper.
    Args:
        chunk_path: Percorso del chunk da trascrivere
        model: Modello Whisper già caricato
        language: Lingua del contenuto
    Returns:
        str: Testo trascritto del chunk (pulito)
    """
    try:
        print(f"  DEBUG: Inizio trascrizione chunk {os.path.basename(chunk_path)}")

        # Verifica che il chunk esista e sia valido
        if not os.path.exists(chunk_path):
            print(f"  ❌ ERRORE: Chunk non trovato: {chunk_path}")
            return ""

        chunk_size = os.path.getsize(chunk_path)
        print(f"  DEBUG: Chunk size: {chunk_size} bytes")

        if chunk_size < 1000:
            print(f"  ❌ ERRORE: Chunk troppo piccolo: {chunk_size} bytes")
            return ""

        # Verifica che il modello sia valido
        if not hasattr(model, 'transcribe'):
            print(f"  ❌ ERRORE: Modello non valido, manca metodo transcribe")
            return ""

        # Trascrive il chunk usando il modello già caricato
        print(f"  DEBUG: Avvio trascrizione con modello {type(model)}")
        try:
            result = model.transcribe(chunk_path, language=language)
            print(f"  DEBUG: Trascrizione completata per {os.path.basename(chunk_path)}")
            return clean_transcription(result['text'])
        except (AttributeError, KeyError) as e:
            if "Linear" in str(e) or any(x in str(e) for x in ["KeyError", "transcribe", "decoder", "encoder"]):
                print(f"  ❌ ERRORE CRITICO: Modello Whisper danneggiato durante la trascrizione")
                print(f"  DEBUG: Errore modello: {e}")
                print("  🔧 RISOLUZIONE AUTOMATICA: Reinstallazione forzata di Whisper in corso...")
                try:
                    # Forza la reinstallazione di Whisper
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "openai-whisper"])
                    print("  ✅ Whisper reinstallato. Riavvia lo script per utilizzare il modello riparato.")
                except subprocess.CalledProcessError:
                    print("  ❌ Impossibile reinstallare automaticamente. Esegui manualmente:")
                    print("  pip install --force-reinstall openai-whisper")
                return ""
            else:
                raise e

    except Exception as e:
        print(f"  ❌ ERRORE nella trascrizione del chunk {os.path.basename(chunk_path)}: {e}")
        print(f"  DEBUG: Tipo errore: {type(e).__name__}")
        import traceback
        print(f"  DEBUG: Traceback: {traceback.format_exc()}")
        return ""

def transcribe_audio_parallel(file_path, model, language='it'):
    """
    Trascrive un file audio dividendo in chunk e processando in parallelo.
    Args:
        file_path: Percorso del file audio da trascrivere
        model: Modello Whisper già caricato
        language: Lingua del contenuto
    Returns:
        str: Testo trascritto completo
    """
    import concurrent.futures
    import time
    from tqdm import tqdm

    print("Avvio trascrizione parallela...")

    # Ottieni la durata per la barra di progresso
    audio_duration = get_audio_duration(file_path)

    # Dividi l'audio in chunk
    chunks = split_audio_into_chunks(file_path)

    if not chunks or len(chunks) == 1:
        # Se non è stato possibile dividere o audio troppo corto, trascrizione singola
        print("Esecuzione trascrizione singola (audio corto o indivisibile)")
        return transcribe_podcast_with_progress(file_path, model, language, parallel=False)

    print(f"⚡ Divisione audio in {len(chunks)} chunk per elaborazione parallela...")

    start_time = time.time()

    try:
        # Crea barra di progresso per la trascrizione parallela
        try:
            pbar = tqdm(total=100,
                       desc="🚀 Elaborazione Parallela",
                       unit="%",
                       ncols=100)
        except Exception as e:
            print(f"Attenzione: errore nell'inizializzazione della barra di progresso: {e}")
            print("Continuo senza barra di progresso...")
            pbar = None

        # Avvia trascrizione parallela dei chunk
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Invia i job per i due chunk
            future1 = executor.submit(transcribe_chunk_parallel, chunks[0], model, language)
            future2 = executor.submit(transcribe_chunk_parallel, chunks[1], model, language)

            # Funzione per aggiornare la barra di progresso durante l'attesa
            def update_progress():
                """Aggiorna la barra di progresso durante l'elaborazione parallela"""
                if pbar is None:
                    return
                while not pbar.disable:
                    elapsed = time.time() - start_time
                    # Calcola il progresso basato sul tempo trascorso vs tempo stimato
                    # I chunk paralleli dovrebbero essere circa 2x più veloci
                    processing_ratio = 0.15  # secondi di processing per secondo di audio
                    estimated_progress = min(95, (elapsed / (audio_duration * processing_ratio / 2)) * 100)

                    if estimated_progress >= pbar.n:
                        # Calcola velocità e tempo rimanente stimato
                        speed = estimated_progress / elapsed if elapsed > 0 else 0
                        remaining = (100 - estimated_progress) / speed if speed > 0 else 0

                        pbar.update(estimated_progress - pbar.n)
                        pbar.set_postfix_str(f"Audio: {audio_duration:.0f}s, Velocità: {speed:.1f}%/s, ETA: {remaining:.0f}s")

                    time.sleep(0.5)  # Aggiorna ogni 0.5 secondi

            # Avvia il thread per l'aggiornamento del progresso
            if pbar:
                progress_thread = threading.Thread(target=update_progress, daemon=True)
                progress_thread.start()

            # Attende i risultati con barra di progresso
            # Timeout aumentato per audio lunghi: 20 minuti per chunk
            chunk_timeout = max(1200, audio_duration // 2 + 300)  # Minimo 20 minuti o metà durata + 5 minuti

            if pbar:
                chunk1_text = future1.result(timeout=chunk_timeout)
                chunk2_text = future2.result(timeout=chunk_timeout)
            else:
                print("Attesa completamento trascrizione chunk 1...")
                chunk1_text = future1.result(timeout=chunk_timeout)
                print("Chunk 1 completato, attesa chunk 2...")
                chunk2_text = future2.result(timeout=chunk_timeout)

        # Unisce i risultati
        full_transcription = chunk1_text.strip() + " " + chunk2_text.strip()

        elapsed = time.time() - start_time
        print(f"✅ Trascrizione parallela completata in {elapsed:.1f} secondi")

        # Chiude la barra di progresso se esiste
        if pbar:
            try:
                pbar.close()
            except:
                pass

        # Pulisce i chunk se sono stati creati
        for chunk in chunks:
            if chunk != file_path and os.path.exists(chunk):
                try:
                    os.remove(chunk)
                    print(f"  Chunk {os.path.basename(chunk)} rimosso")
                except Exception as e:
                    print(f"  Attenzione: impossibile rimuovere {chunk}: {e}")

        # Rimuovi la directory _temp se vuota
        temp_dir = os.path.join(os.path.dirname(file_path), "_temp")
        if os.path.exists(temp_dir):
            try:
                # Verifica se la directory è vuota
                if not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
                    print(f"  Directory temporanea {os.path.basename(temp_dir)} rimossa")
            except Exception as e:
                print(f"  Attenzione: impossibile rimuovere la directory temporanea: {e}")

        return full_transcription

    except concurrent.futures.TimeoutError:
        print("Timeout nella trascrizione parallela, fallback a trascrizione singola")
        return transcribe_podcast_with_progress(file_path, model, language, parallel=False)
    except Exception as e:
        print(f"Errore nella trascrizione parallela: {e}, fallback a trascrizione singola")
        return transcribe_podcast_with_progress(file_path, model, language, parallel=False)

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
    print(f"  DEBUG: transcribe_podcast_with_progress chiamato per {os.path.basename(file_path)}")

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
        return transcribe_audio_parallel(file_path, model, language)

    # Altrimenti, trascrizione singola tradizionale
    start_time = time.time()

    # Barra di progresso per la trascrizione singola
    try:
        from tqdm import tqdm as tqdm_class
        pbar = tqdm_class(total=100,
                   desc="🎵 Trascrizione Audio",
                   unit="%",
                   ncols=100)
    except Exception as e:
        print(f"Attenzione: errore nell'inizializzazione della barra di progresso: {e}")
        print("Continuo senza barra di progresso...")
        pbar = None
    
    # Avvia la trascrizione con soppressione del warning FP16
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

        def update_progress():
            """Aggiorna la barra di progresso basata su stime temporali"""
            import time

            if pbar is None:
                return

            # Simula il progresso basato sulla durata stimata
            # Whisper processa circa 1 secondo di audio ogni 0.1-0.2 secondi su CPU
            processing_ratio = 0.15  # secondi di processing per secondo di audio

            while not pbar.disable:
                elapsed = time.time() - start_time
                # Calcola il progresso basato sul tempo trascorso vs tempo stimato
                estimated_progress = min(95, (elapsed / (audio_duration * processing_ratio)) * 100)

                if estimated_progress >= pbar.n:
                    # Calcola velocità e tempo rimanente stimato
                    speed = estimated_progress / elapsed if elapsed > 0 else 0
                    remaining = (100 - estimated_progress) / speed if speed > 0 else 0

                    pbar.update(estimated_progress - pbar.n)
                    pbar.set_postfix_str(f"Audio: {audio_duration:.0f}s, Velocità: {speed:.1f}%/s, ETA: {remaining:.0f}s")

                time.sleep(0.5)  # Aggiorna ogni 0.5 secondi

        # Avvia il thread per l'aggiornamento del progresso
        if pbar:
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()

        # Verifica che il file esista prima della trascrizione
        if not os.path.exists(file_path):
            print(f"  ❌ ERRORE: File non trovato per trascrizione: {file_path}")
            return ""

        # Esegue la trascrizione
        print(f"  DEBUG: Esecuzione trascrizione per {os.path.basename(file_path)}")
        try:
            result = model.transcribe(file_path, language=language)
            print(f"  DEBUG: Trascrizione completata con successo")
        except (AttributeError, KeyError) as e:
            if "Linear" in str(e) or any(x in str(e) for x in ["KeyError", "transcribe", "decoder", "encoder"]):
                print(f"  ❌ ERRORE CRITICO: Modello Whisper danneggiato durante la trascrizione")
                print(f"  DEBUG: Errore modello: {e}")
                print("  🔧 RISOLUZIONE AUTOMATICA: Reinstallazione forzata di Whisper in corso...")
                try:
                    # Forza la reinstallazione di Whisper
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "openai-whisper"])
                    print("  ✅ Whisper reinstallato. Riavvia lo script per utilizzare il modello riparato.")
                except subprocess.CalledProcessError:
                    print("  ❌ Impossibile reinstallare automaticamente. Esegui manualmente:")
                    print("  pip install --force-reinstall openai-whisper")
                return ""
            else:
                raise e

    # Completa la barra di progresso
    elapsed = time.time() - start_time
    if pbar:
        pbar.update(100 - pbar.n)  # Completa fino al 100%
        pbar.set_postfix_str(f"Tempo: {elapsed:.1f}s, Durata: {audio_duration:.1f}s")
        try:
            pbar.close()
        except:
            pass

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

def main(podcast_dir, model_name='medium', language='it', parallel=False):
    """
    Funzione principale con barra di progresso e ETA.
    Args:
        podcast_dir: Directory contenente i file audio
        model_name: Nome del modello Whisper da utilizzare
        language: Lingua del contenuto audio
        parallel: Se True, utilizza processamento parallelo per velocizzare
    """
    # Importa i moduli necessari
    whisper, tqdm = import_required_modules()

    # Carica il modello Whisper con fallback automatico
    print(f"Caricamento del modello {model_name}...")

    # Lista di modelli da provare in ordine di preferenza
    model_names = [model_name, 'base', 'small', 'tiny']

    model = None
    for attempt_model in model_names:
        try:
            print(f"  DEBUG: Tentativo con modello {attempt_model}")
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
                model = whisper.load_model(attempt_model)

            # Verifica che il modello sia valido
            if hasattr(model, 'transcribe'):
                print(f"✅ SUCCESSO: Modello {attempt_model} caricato correttamente")
                if attempt_model != model_name:
                    print(f"⚠️  ATTENZIONE: Usato modello {attempt_model} invece di {model_name}")
                break
            else:
                print(f"❌ ERRORE: Modello {attempt_model} caricato ma non valido")
                model = None

        except Exception as e:
            print(f"❌ ERRORE: Impossibile caricare il modello {attempt_model}: {e}")
            model = None
            continue

    if model is None:
        print(f"❌ ERRORE CRITICO: Impossibile caricare alcun modello Whisper valido")
        print("Verifica l'installazione di Whisper e PyTorch")
        print("Se il problema persiste, prova a reinstallare:")
        print("  pip uninstall openai-whisper torch torchvision torchaudio")
        print("  pip install openai-whisper")
        return

    print(f"DEBUG: Modello verificato, pronto per la trascrizione")

    # Conta i file da elaborare
    total_files = count_supported_audio_files(podcast_dir)
    
    if total_files == 0:
        print("Nessun file audio supportato da elaborare trovato.")
        print("Formati supportati: WAV, MP3, FLAC, OGG, M4A, AAC, WMA, Opus, AIFF, WebM, MP4")
        return
    
    print(f"\nTrovati {total_files} file da trascrivere.")
    
    processed_files = 0
    start_time = time.time()
    processed_file_list = []  # Lista per tracciare file già elaborati
    
    # Barra di progresso principale per tutti i file
    try:
        main_pbar = tqdm(total=total_files,
                        desc="📁 Elaborazione File",
                        unit="file",
                        ncols=100)
    except Exception as e:
        print(f"Attenzione: errore nell'inizializzazione della barra di progresso principale: {e}")
        print("Continuo senza barra di progresso...")
        main_pbar = None
    
    for root, dirs, files in os.walk(podcast_dir):
        # Salta la directory _temp per evitare di processare i chunk temporanei
        dirs[:] = [d for d in dirs if d != '_temp']

        for file_name in files:
            file_path = os.path.join(root, file_name)
            base_name, ext = os.path.splitext(file_name)

            # Verifica se il formato è supportato
            if not is_audio_format_supported(file_path):
                continue

            output_file_name = base_name + '.txt'
            output_path = os.path.join(root, output_file_name)

            # Verifica se la trascrizione esiste già e contiene dati significativi
            if os.path.exists(output_path):
                txt_size = os.path.getsize(output_path)
                print(f"  DEBUG: File .txt esistente: {output_path} ({txt_size} bytes)")
                if txt_size > 10:  # Più di 10 byte = probabilmente contiene trascrizione
                    print(f"  ⏭️  Trascrizione già esistente per: {file_name} ({txt_size} bytes)")
                    if main_pbar:
                        main_pbar.update(1)
                    continue
                else:
                    print(f"  ⚠️  File .txt esistente ma vuoto o quasi ({txt_size} bytes) - rielaboro")
            else:
                print(f"  DEBUG: Nessun file .txt esistente per {file_name}")

            # Verifica se il file è già stato elaborato in questa sessione
            if file_path in processed_file_list:
                print(f"  ⏭️  File già elaborato in questa sessione: {file_name}")
                if main_pbar:
                    main_pbar.update(1)
                continue

            print(f"  📝  Elaborazione file: {file_name}")
            print(f"  DEBUG: File path: {file_path}")
            print(f"  DEBUG: File esiste: {os.path.exists(file_path)}")
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  DEBUG: File size: {file_size} bytes")
                if file_size < 1000:  # Meno di 1KB è probabilmente non valido
                    print(f"  ❌ ERRORE: File troppo piccolo ({file_size} bytes), probabilmente non è un file audio valido")
                    if main_pbar:
                        main_pbar.update(1)
                    continue
            else:
                print(f"  ❌ ERRORE: File non esiste: {file_path}")
                if main_pbar:
                    main_pbar.update(1)
                continue

            # File WAV da utilizzare per la trascrizione (originale o convertito)
            wav_file_path = None
            converted_file_path = None

            try:
                file_start_time = time.time()

                # Aggiorna la descrizione con il file corrente
                if main_pbar:
                    main_pbar.set_description(f"Elaborando: {file_name[:30]}...")

                # Se non è WAV, convertilo
                if ext.lower() != '.wav':
                    print(f"  DEBUG: Conversione richiesta per {file_name}")
                    converted_file_path = os.path.join(root, base_name + '_converted.wav')
                    print(f"  DEBUG: Converted file path: {converted_file_path}")
                    if convert_audio_to_wav(file_path, converted_file_path):
                        wav_file_path = converted_file_path
                        print(f"  Conversione completata: {file_name}")
                    else:
                        print(f"  ❌ Impossibile convertire {file_name}, salto...")
                        if main_pbar:
                            main_pbar.update(1)
                        continue
                else:
                    # È già WAV, usa il file originale
                    print(f"  DEBUG: File già WAV, uso originale")
                    wav_file_path = file_path

                print(f"  DEBUG: wav_file_path impostato: {wav_file_path}")

                # Procedi con la trascrizione
                print(f"  DEBUG: Inizio trascrizione per {os.path.basename(wav_file_path)}")
                transcription = transcribe_podcast_with_progress(wav_file_path, model, language, parallel)
                print(f"  DEBUG: Trascrizione completata, lunghezza: {len(transcription)} caratteri")
                print(f"  DEBUG: Salvataggio trascrizione in {output_path}")
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
                if main_pbar:
                    main_pbar.update(1)
                    main_pbar.set_postfix_str(f"Tempo/file: {file_elapsed:.1f}s, ETA: {eta_formatted}, Totale: {format_time(elapsed_total)}")

                print(f"\n✅ Completato: {file_name}")
                print(f"💾 Salvato in: {output_path}")
                print(f"⏱️  Tempo impiegato: {file_elapsed:.1f} secondi")

            except Exception as e:
                print(f"\n❌ Errore durante la trascrizione di {file_name}: {e}")
                if main_pbar:
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
    # Conta file saltati
    skipped_files = total_files - processed_files

    print(f"\n🎉 Trascrizione completata!")
    print(f"📊 File elaborati: {processed_files}")
    if skipped_files > 0:
        print(f"⏭️  File saltati (già esistenti): {skipped_files}")
    print(f"📁 Totale file trovati: {total_files}")
    print(f"⏱️  Tempo totale: {format_time(total_elapsed)}")
    if processed_files > 0:
        print(f"📈 Tempo medio per file: {total_elapsed/processed_files:.1f} secondi")

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

    # Aggiorna pip e installa correttamente whisper e tqdm (solo una volta)
    try:
        upgrade_pip_and_install_packages()
    except Exception as e:
        print(f"Errore durante l'aggiornamento dei pacchetti: {e}")

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