# Analisi e elenco ordinato delle estensioni file in una directory.
import os

def get_file_extensions(folder_path):
    extensions = set()  # Utilizziamo un set per evitare duplicati
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()  # Otteniamo l'estensione e la convertiamo in minuscolo
            extensions.add(ext)
    
    return extensions

def print_extensions(extensions):
    print("Estensioni dei file trovate:")
    for ext in sorted(extensions):
        if ext:  # Stampa solo se l'estensione non è vuota
            print(ext)

def main():
    folder_path = input("Inserisci il percorso della cartella: ").strip()
    if os.path.isdir(folder_path):
        extensions = get_file_extensions(folder_path)
        print_extensions(extensions)
    else:
        print("Il percorso inserito non è valido. Per favore riprova.")

if __name__ == "__main__":
    main()
