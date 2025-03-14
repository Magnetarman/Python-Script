import os
import whisper
from pydub import AudioSegment

def convert_to_wav(input_file, output_dir):
    """
    Converte un file audio in formato .wav usando pydub.
    """
    file_name, ext = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.join(output_dir, file_name + '.wav')
    
    try:
        print(f"Conversione di {input_file} in formato .wav...")
        if ext == ".mp3":
            audio = AudioSegment.from_mp3(input_file)
        elif ext == ".flac":
            audio = AudioSegment.from_file(input_file, format="flac")
        elif ext == ".ogg":
            audio = AudioSegment.from_ogg(input_file)
        else:
            raise ValueError(f"Formato {ext} non supportato.")
        
        audio.export(output_file, format="wav")
        print(f"File convertito: {output_file}")
        return output_file
    except Exception as e:
        print(f"Errore durante la conversione di {input_file}: {e}")
        return None

def transcribe_podcast(file_path, model_name='medium', language='it'):
    """
    Trascrive un file audio utilizzando il modello Whisper.
    """
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

            # Supportati formati audio
            supported_formats = ['.wav', '.mp3', '.flac', '.ogg']
            
            if ext.lower() in supported_formats:
                # Se non è un file .wav, convertilo
                if ext.lower() != '.wav':
                    file_path = convert_to_wav(file_path, root)
                    if file_path is None:
                        continue  # Salta se la conversione fallisce
                
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
    podcast_dir = input("Inserisci il percorso della cartella contenente i podcast: ").strip()
    if os.path.isdir(podcast_dir):
        main(podcast_dir)
        print("Trascrizione completata.")
    else:
        print("Il percorso inserito non è valido. Per favore riprova.")
