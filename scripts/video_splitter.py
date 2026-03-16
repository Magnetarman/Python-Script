"""
Suddivide un file video in spezzoni di massimo 30 minuti tramite ffmpeg.
"""

import os
import subprocess
import sys

def split_video():
    print("--- Suddividi Video in Spezzoni da 30 Minuti ---")
    video_path = input("Inserisci il percorso completo del file video: ").strip()
    
    # Rimuove apici che potrebbero essere aggiunti trascinando il file nel terminale
    if video_path.startswith('"') and video_path.endswith('"'):
        video_path = video_path[1:-1]
    
    if not os.path.isfile(video_path):
        print(f"Errore: Il file '{video_path}' non esiste o non è stato trovato.")
        return

    # Estrazione di directory, nome e estensione originale
    directory = os.path.dirname(os.path.abspath(video_path))
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)

    # Creazione del pattern di output: es. video_originale_part001.mp4
    output_pattern = os.path.join(directory, f"{name}_part%03d{ext}")

    print(f"\nPreparazione per suddividere: {filename}")
    print(f"I segmenti verranno creati nella cartella: {directory}\n")

    # Costruzione del comando FFmpeg.
    # Usiamo il muxer "segment" per dividere il video senza ricodificarlo (-c copy),
    # il che rende il processo estremamente rapido mantenendo la qualità originale.
    # segment_time = 1800 secondi (30 minuti).
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-c", "copy",
        "-map", "0",
        "-segment_time", "1800",
        "-f", "segment",
        "-reset_timestamps", "1",
        output_pattern
    ]

    try:
        # Esegue il comando lasciando che l'output di FFmpeg venga mostrato all'utente
        subprocess.run(cmd, check=True)
        print("\n[OK] Suddivisione completata con successo!")
    except FileNotFoundError:
        print("\n[ERRORE] Eseguibile 'ffmpeg' non trovato.")
        print("Assicurati che FFmpeg sia installato e aggiunto alla variabile d'ambiente PATH del sistema.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRORE] Il processo FFmpeg ha riportato un errore (codice: {e.returncode}).")
    except Exception as e:
        print(f"\n[ERRORE] Si è verificato un problema imprevisto: {e}")

if __name__ == "__main__":
    split_video()
