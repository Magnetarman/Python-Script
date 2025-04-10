# Rimozione file non musicali e pulizia cartelle vuote in una directory.
import os
import re

# Definisci le estensioni dei file musicali che vuoi preservare
musical_extensions = re.compile(r'\.(flac|opus|mp3|m4a|aac)$', re.IGNORECASE)

def delete_non_music_files(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            # Se il file non ha un'estensione musicale, viene eliminato
            if not musical_extensions.search(name):
                print(f"Deleting file: {file_path}")
                os.remove(file_path)
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            # Se la cartella è vuota, viene eliminata
            if not os.listdir(dir_path):
                print(f"Deleting empty directory: {dir_path}")
                os.rmdir(dir_path)

def main():
    folder_path = input("Inserisci il percorso della cartella: ").strip()
    if os.path.isdir(folder_path):
        delete_non_music_files(folder_path)
        print("Pulizia completata.")
    else:
        print("Il percorso inserito non è valido. Per favore riprova.")

if __name__ == "__main__":
    main()
