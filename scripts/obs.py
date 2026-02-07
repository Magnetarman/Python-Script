import os
from pydub import AudioSegment, effects
from pydub.utils import mediainfo

def get_min_bitrate(files):
    """Analizza i file e restituisce il bitrate più basso trovato (in kbps)."""
    bitrates = []
    for f in files:
        try:
            info = mediainfo(f)
            # Il bitrate è riportato in bit/s (es. 128000)
            bitrate = int(info.get('bit_rate', 192000)) 
            bitrates.append(bitrate)
        except:
            continue
    
    if not bitrates:
        return "128k"
    
    # Troviamo il minimo e convertiamo in formato 'k' (es. 128k)
    min_k = int(min(bitrates) / 1000)
    return f"{min_k}k"

def process_audio_optimized():
    output_filename = "risultato_ottimizzato.mp3"
    files = sorted([f for f in os.listdir('.') if f.endswith('.mp3') and f != output_filename])

    if not files:
        print("Nessun file MP3 trovato!")
        return

    # 1. Analisi del bitrate minimo per risparmiare spazio
    target_bitrate = get_min_bitrate(files)
    print(f"Bitrate ottimizzato rilevato: {target_bitrate}")

    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=3000)

    print(f"Elaborazione di {len(files)} file...")

    for f in files:
        try:
            # Caricamento e standardizzazione
            audio = AudioSegment.from_mp3(f).set_frame_rate(44100).set_channels(2)
            
            # 2. Normalizzazione del volume (porta il picco a 0 dB)
            audio = effects.normalize(audio)
            
            print(f"Aggiungendo e normalizzando: {f}")
            combined += audio + silence
        except Exception as e:
            print(f"Errore su {f}: {e}")

    # 3. Esportazione finale
    print(f"Esportazione in corso ({target_bitrate}, CBR)...")
    combined.export(
        output_filename, 
        format="mp3", 
        bitrate=target_bitrate, 
        parameters=["-write_xing", "0"] # Forza CBR puro per compatibilità timer
    )

    print("-" * 30)
    print(f"COMPLETATO!")
    print(f"File: {output_filename}")
    print(f"Peso ottimizzato con bitrate: {target_bitrate}")
    print(f"Durata totale: {len(combined) / 1000} secondi.")
    print("-" * 30)

if __name__ == "__main__":
    process_audio_optimized()