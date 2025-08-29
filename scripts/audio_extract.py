# Estrazione tracce audio .flac da file .mkv (anche ricorsiva).
import os
import subprocess

def get_audio_tracks(video_path):
    cmd = [
        "ffprobe", "-i", video_path, "-show_entries", "stream=index:stream_tags=language", "-select_streams", "a", "-of", "csv=p=0"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    tracks = result.stdout.strip().split("\n")
    return [track.split(',') for track in tracks if track]

def extract_audio(video_path, track_number, output_format="flac"):
    output_path = os.path.splitext(video_path)[0] + f"_track{track_number}.{output_format}"
    cmd = [
        "ffmpeg", "-i", video_path, "-map", f"0:a:{track_number}", "-c:a", "flac", output_path
    ]
    subprocess.run(cmd)
    print(f"Audio estratto: {output_path}")

def process_directory(directory, track_number):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mkv"):
                video_path = os.path.join(root, file)
                print(f"Elaborazione di: {video_path}")
                extract_audio(video_path, track_number)

def main():
    video_path = input("Inserisci il percorso del file MKV o della directory: ").strip()
    if not os.path.exists(video_path):
        print("Il percorso specificato non esiste.")
        return
    
    if os.path.isfile(video_path):
        tracks = get_audio_tracks(video_path)
        if not tracks:
            print("Nessuna traccia audio trovata.")
            return
        
        print("Tracce audio trovate:")
        for i, track in enumerate(tracks):
            lang = track[1] if len(track) > 1 else "sconosciuto"
            print(f"{i}: Traccia {track[0]} ({lang})")
        
        try:
            track_number = int(input("Inserisci il numero della traccia da esportare: "))
            extract_audio(video_path, track_number)
        except ValueError:
            print("Numero traccia non valido.")
    else:
        track_number = int(input("Inserisci il numero della traccia da esportare: "))
        recursive = input("Vuoi elaborare tutti i file MKV nella directory in modo ricorsivo? (s/n): ").strip().lower()
        if recursive == 's':
            process_directory(video_path, track_number)
        else:
            for file in os.listdir(video_path):
                if file.endswith(".mkv"):
                    video_file = os.path.join(video_path, file)
                    extract_audio(video_file, track_number)

if __name__ == "__main__":
    while True:
        main()
        scelta = input("\nUtilizza di nuovo lo script digitando 1 o premi 0 per ritornare a main.py: ").strip()
        if scelta == '1':
            continue
        elif scelta == '0':
            break
        else:
            print("Scelta non valida. Inserire 1 o 0.")
