import os
import whisper

def transcribe_podcast(file_path, model_name='medium', language='it'):
    # Carica il modello Whisper
    model = whisper.load_model(model_name)
    
    # Trascrivi l'audio con Whisper
    result = model.transcribe(file_path, language=language)
    
    # Ottieni il testo trascritto
    transcription = result['text']
    
    return transcription

def save_transcription(transcription, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)

def main(podcast_dir):
    for root, dirs, files in os.walk(podcast_dir):
        for file_name in files:
            if file_name.endswith('.wav'):
                file_path = os.path.join(root, file_name)
                output_file_name = os.path.splitext(file_name)[0] + '.txt'
                output_path = os.path.join(root, output_file_name)

                # Verifica se il file di trascrizione esiste e ha un peso maggiore di 1 byte
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1:
                    print(f'Saltato {file_name}, il file di trascrizione {output_file_name} esiste già.')
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
